import asyncio
from typing import *
from os import environ
from mangum import Mangum
from uuid import uuid4
from fastapi import *
from fastapi.exceptions import *
from fastapi.responses import *
from pydantic import *
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch

load_dotenv()

class env: # pylint: disable=all
    """Environment Variables"""
    AUTH0_DOMAIN = environ.get("AUTH0_DOMAIN")
    GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
    HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    CLOUD_ID=environ.get("CLOUD_ID")
    USER="elastic"
    PASSWORD=environ.get("PASSWORD")

class ElasticModel(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid4()))
    document: Mapping[str,Any]

    class Config(BaseConfig):
        arbitrary_types_allowed = True
        extra = Extra.allow

    @property
    def es(self):
        return AsyncElasticsearch(
            cloud_id=env.CLOUD_ID,http_auth=(env.USER, env.PASSWORD)
        )

    @property
    def index(self):
        return self.__class__.__name__.lower()+"s"

    async def save(self):
        """Save the document to ElasticSearch"""
        async with self.es as es:
            await es.index(index=self.index, id=self.id, document=self.document)

    async def search(self, query: str):
        """Search the ElasticSearch index"""
        return await self.es.search(index=self.index, q=query)

class WebSite(ElasticModel):
    ...

class SearchResult(ElasticModel):
    ...

class GitHubRepo(ElasticModel):
    ...

class APIClient:
    base_url: Optional[str] = "https://api.github.com"
    headers: Optional[Dict[str, str]] = {
        "Authorization": f"token {env.GITHUB_TOKEN}",
    }

    def __init__(self, base_url:Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url if base_url else self.base_url
        self.headers = headers if headers else self.headers

    async def get(self, url: str, params:Optional[ Dict[str, str]] = None) -> Dict[str, Any]:
        async with ClientSession(headers=self.headers) as client_session:
            async with client_session.get(f"{self.base_url}{url}", params=params) as response:
                res = await response.json()
                await client_session.close()
                return res
            
    async def html(self, domain: str) -> str:
        async with ClientSession(headers=env.HEADERS) as client_session:
            async with client_session.get(f"https://{domain}") as response:
                return await response.text(encoding="utf-8")
    
    async def soup(self, domain: str) -> BeautifulSoup:
        return BeautifulSoup(await self.html(domain), "lxml")
    
class ServerlessApp(FastAPI):
    """FastAPI app."""
    def __init__(self):
        super().__init__()
        self.title="CloudScraper"
        self.description="⚡ Lightning Fast Web Scraping\n ☁️ Powered by CloudSearch"
        self.version="0.0.1"

app = ServerlessApp()
    
@app.get("/github/{q}")
async def github(q:str, sort:str="stars", order:str="desc", page:int=1, per_page:int=32)->List[Dict[str,Any]]:
    try:
        api_session = APIClient(base_url="https://api.github.com", headers={
            "Authorization": f"token {env.GITHUB_TOKEN}",
        })
        response = await api_session.get(f"/search/repositories?q={q}&sort={sort}&order={order}&page={page}&per_page={per_page}")
        documents = [{
            "name": response["items"][i]["name"],
            "owner": response["items"][i]["owner"]["login"],
            "avatar": response["items"][i]["owner"]["avatar_url"],
            "type": response["items"][i]["owner"]["type"],
            "description": response["items"][i]["description"],
            "languages": [{k:v} for k,v in (await api_session.get(f"/repos/{response['items'][i]['full_name']}/languages")).items()],
            "size": response["items"][i]["size"],
            "stars": response["items"][i]["stargazers_count"],
            "forks": response["items"][i]["forks_count"],
            "issues": response["items"][i]["open_issues_count"],
            "topics": response["items"][i]["topics"],
            "url": response["items"][i]["html_url"]
        } for i in range(len(response["items"]))]
        await asyncio.gather(*[GitHubRepo(document=document).save() for document in documents])
        for document in documents:
            if document["type"] == "Organization":
                documents.remove(document)
            else:
                document.pop("type")
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/search/{lang}/{query}/{page}")
async def search(query:str,lang:str="en-US",page:int=1)->List[Dict[str,Any]]:
    """Search page"""
    api_session = APIClient(base_url="https://www.google.com/search", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"})
    html = await api_session.html(f"google.com/search?q={query}&start={page*10}&hl={lang}")
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for result in soup.find_all("div", class_="yuRUbf"):
        link = result.find("a", href=True)
        title = result.find("h3", text=True)
        results.append({
            "summary": title.text,
            "url": link["href"],
        })
        await asyncio.gather(*[SearchResult(document=result).save() for result in results])
    return results

@app.get("/")
async def auth(request: Request):
    """Auth dependency"""
    try:
        token = request.headers["Authorization"].split(" ")[1]
        api_session = APIClient(base_url=f"https://{env.AUTH0_DOMAIN}", headers={"Authorization": f"Bearer {token}"})
        response = await api_session.get("/userinfo")
        return response
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@app.get("/crawl/{domain}")
async def crawl(domain:str):
    try:
        async with ClientSession() as client_session:
            async with client_session.get(f"https://{domain}") as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                images = []
                links = []
                for img in soup.find_all("img",src=True):
                    if img["src"].startswith("http") and img["src"] not in images:
                        images.append(img["src"])
                    elif img["src"].startswith("/") and f"https://{domain}{img['src']}" not in images:
                        images.append(f"https://{domain}{img['src']}")
                    else:
                        pass
                for link in soup.find_all("a", href=True):
                    if link["href"].startswith("http") and link["href"] not in links:
                        links.append(link["href"])
                    elif link["href"].startswith("/") and link["href"] not in links:
                        links.append(f"https://{domain}{link['href']}")
                    else:
                        pass
                website = {
                    "domain": domain,
                    "images": images,
                    "links": links,
                    "text": soup.get_text().strip().replace("\n"," ").replace("\t"," ").replace("\r"," "),
                }
                await asyncio.gather(*[WebSite(document=website).save()])
                return website
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
handler = Mangum(app)
