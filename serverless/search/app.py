import asyncio
import lxml
from os import environ
from dotenv import load_dotenv
from typing import *
from fastapi import *
from fastapi.responses import *
from elasticsearch import AsyncElasticsearch
from pydantic import *
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from uuid import uuid4
load_dotenv()

class Client(BaseModel):
    base_url:Union[str, AnyHttpUrl] = "https://api.github.com/"
    headers:Dict[str,str] = {"Authorization": f"token {environ['GITHUB_TOKEN']}"}
    
    async def get(self, url:str) -> str:
        async with ClientSession(headers=self.headers) as session:
            async with session.get(self.base_url + url) as response:
                return await response.json()
    
    async def soup(self, url:str) -> BeautifulSoup:
        return BeautifulSoup(await self.get(url), "lxml")


app = FastAPI()

@app.get("/{q}")
async def get_repos(q:str, sort:str="stars", order:str="desc", page:int=1, per_page:int=10):
    """Gets repos with several parameters including good practices defaults
    Returns a list of repos with their URL fields"""
    client = Client()
    response =  await client.get(f"search/repositories?q={q}&sort={sort}&order={order}&page={page}&per_page={per_page}")
    repos = response["items"]
    foo = repos[0]
    print(len(foo.items()))
    urls = [{k:v} for k,v in foo.items() if k in ["contents_url","blobs_url","languages_url","tags_url"]]
    for url in urls:
        for k,v in url.items():
            url[k] = await client.get(v.split("{")[0].replace("https://api.github.com/",""))
    return urls
