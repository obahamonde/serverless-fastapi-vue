import asyncio
import lxml
from typing import *
from decimal import Decimal
from datetime import datetime
from uuid import uuid4, UUID
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Binary
from fastapi import *
from fastapi.exceptions import *
from fastapi.responses import *
from fastapi.staticfiles import StaticFiles
from pydantic import *
from aioboto3 import Session
from boto3 import Session as boto3Session
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from dotenv import load_dotenv
from uuid import uuid4
from os import environ

load_dotenv()

AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = environ.get("AWS_DEFAULT_REGION")
AWS_SES_EMAIL = environ.get("AWS_SES_EMAIL")
AWS_S3_BUCKET = environ.get("AWS_S3_BUCKET")
AUTH0_DOMAIN = environ.get("AUTH0_DOMAIN")
GH_API_TOKEN = environ.get("GH_API_TOKEN")
GH_API_URL = environ.get("GH_API_URL")
HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

class AWSClient:
    def __init__(self):
        credentials = boto3Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_DEFAULT_REGION
        ).client("sts").get_session_token()['Credentials']
        self.session = Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=AWS_DEFAULT_REGION
        )

    async def upload(self,sub:str, file:UploadFile=File(...))->HttpUrl:
        async with self.session.client("s3") as client:
            await client.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=f"{sub}/{file.filename}",
                Body=file.file.read(),
                ACL="public-read",
                ContentType=file.content_type
            )
            return f"https://s3.amazonaws.com/{AWS_S3_BUCKET}/{sub}/{file.filename}"

    async def list_uploads(self,sub:str)->List[Dict[str,Any]]:
        async with self.session.client("s3") as client:
            return await client.list_objects_v2(
                Bucket=AWS_S3_BUCKET,
                Prefix=sub
            )

    async def delete_upload(self, key:str)->Dict[str,Any]:
        async with self.session.client("s3") as client:
            return await client.delete_object(
                Bucket=AWS_S3_BUCKET,
                Key=key
            )

    async def send_email(self, email:str, subject:str, body:str)->Dict[str,Any]:
        async with self.session.client("ses") as client:
            return await client.send_email(
                Source=AWS_SES_EMAIL,
                Destination={
                    "ToAddresses": [AWS_SES_EMAIL]
                },
                Message={
                    "Subject": {
                        "Data": f'{subject}<{email}>'
                    },
                    "Body": {
                        "Text": {
                            "Data": body
                        }
                    }
                }
            )

    async def translate(self, text:str, source:str, target:str)->Dict[str,Any]:
        async with self.session.client("translate") as client:
            return await client.translate_text(
                Text=text,
                SourceLanguageCode=source,
                TargetLanguageCode=target
            )

    async def comprehend(self, text:str)->Dict[str,Any]:
        async with self.session.client("comprehend") as client:
            return await client.detect_sentiment(
                Text=text,
                LanguageCode="en"
            )

    async def rekognition(self, file:UploadFile=File(...))->Dict[str,Any]:
        async with self.session.client("rekognition") as client:
            return await client.detect_labels(
                Image={
                    "Bytes": file.file.read()
                }
            )

    async def polly(self, text:str)->Dict[str,Any]:
        async with self.session.client("polly") as client:
            return await client.synthesize_speech(
                OutputFormat="mp3",
                Text=text,
                VoiceId="Joanna"
            )

    async def transcribe(self, sub:str, lang:str="es", file:UploadFile=File(...))->Dict[str,Any]:
        async with self.session.client("transcribe") as client:
            url = await self.upload(sub, file)
            return await client.start_transcription_job(
                TranscriptionJobName=f"{sub}-{file.filename}",
                LanguageCode=lang,
                MediaFormat="mp3",
                Media={
                    "MediaFileUri": url
                },
                OutputBucketName=AWS_S3_BUCKET
            )
    async def syntax(self, text:str, lang:str="en")->Dict[str,Any]:
        async with self.session.client("comprehend") as client:
            return await client.detect_syntax(
                Text=text,
                LanguageCode=lang
            )
    
    async def create_bot(self)->Dict[str,Any]:
        async with self.session.client("lex-models") as client:
            return await client.put_bot(
                name="test",
                description="test",
                intents=[
                    {
                        "intentName": "test",
                        "intentVersion": "$LATEST"
                    }
                ],
                clarificationPrompt={
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "Can you repeat that?"
                        }
                    ],
                    "maxAttempts": 2
                },
                abortStatement={
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "Sorry, I can't understand the input. Goodbye!"
                        }
                    ]
                },
                idleSessionTTLInSeconds=300,
                voiceId="Joanna",
                checksum="string",
                processBehavior="BUILD",
                locale="en-US",
                childDirected=False,
                enableModelImprovements=True
            )


session = AWSClient().session

class DynaModel(BaseModel):
    def __init__(self,**data: Any) -> None:
        super().__init__(**data)  
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = Extra.allow
        json_encoders = {
            datetime: str,
            Decimal: float,
            Binary: bytes,
            HttpUrl: str,
            EmailStr: str,
            IPvAnyAddress: str,
            IPvAnyInterface: str,
            IPvAnyNetwork: str
        }

    @property
    def name(self):
        return self.__class__.__name__.lower()+"s"

    @property
    def pk(self):
        for field in self.__fields__:
            if self.__fields__[field].field_info.extra.get("pk"):
                return self.dict()[field]

    @property
    def sk(self):
        for field in self.__fields__:
            if self.__fields__[field].field_info.extra.get("sk"):
                return self.dict()[field]
    
    @property
    def _pk(self):
        for field in self.__fields__:
            if self.__fields__[field].field_info.extra.get("pk"):
                return field
    
    @property
    def _sk(self):
        for field in self.__fields__:
            if self.__fields__[field].field_info.extra.get("sk"):
                return field        

    @property
    def gsi(self):
        gsis: List[str] = []
        for field in self.__fields__:
            if self.__fields__[field].field_info.extra.get("gsi"):
                gsis.append(field)
        return [self.dict()[gsi] for gsi in gsis]   
    
    async def get(self)->JSONResponse:
        """Find unique item by primary key."""
        async with session.resource("dynamodb") as dynamodb:
            table = await dynamodb.Table(self.name)
            response = await table.get_item(
                Key={
                    self._pk: self.pk,
                    self._sk: self.sk
                }
            )
            return response.pop("Item")
            
    async def put(self)->JSONResponse:
        """Create new item."""
        async with session.resource("dynamodb") as dynamodb:
            table = await dynamodb.Table(self.name)
            await table.put_item(
                Item=self.dict()
            )
            return await self.get()
    
    async def update(self)->JSONResponse:
        """Update item."""
        async with session.resource("dynamodb") as dynamodb:
            table = await dynamodb.Table(self.name)
            await table.update_item(
                Key={
                    self._pk: self.pk,
                    self._sk: self.sk
                },
                UpdateExpression="set #n=:v",
                ExpressionAttributeNames={"#n": "name"},
                ExpressionAttributeValues={":v": "new name"}
            )
            return await self.get()
        
    async def delete(self)->JSONResponse:
        """Delete item."""
        async with session.resource("dynamodb") as dynamodb:
            table = await dynamodb.Table(self.name)
            await table.delete_item(
                Key={
                    self._pk: self.pk,
                    self._sk: self.sk
                }
            )
            return await self.get()
        
    async def query(self)->JSONResponse:
        """Query items."""
        async with session.resource("dynamodb") as dynamodb:
            table = await dynamodb.Table(self.name)
            response = await table.query(
                KeyConditionExpression=Key(self._pk).eq(self.pk)
            )
            return response.pop("Items")
        
    async def scan(self)->JSONResponse:
        """Scan items."""
        async with session.resource("dynamodb") as dynamodb:
            table = await dynamodb.Table(self.name)
            response = await table.scan()
            return response.pop("Items")

class Website(BaseModel):
    url: str
    text: str
    links: List[str]
    images: List[str]

class APIClient:
    base_url: Optional[str] = GH_API_URL
    headers: Optional[Dict[str, str]] = GH_API_TOKEN

    def __init__(self, base_url: str = None, headers: Dict[str, str] = None):
        self.base_url = base_url if base_url else self.base_url
        self.headers = headers if headers else self.headers
    async def get(self, url: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        async with ClientSession(headers=self.headers) as session:
            async with session.get(f"{self.base_url}{url}", params=params) as response:
                return await response.json()

    async def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with ClientSession(headers=self.headers) as session:
            async with session.post(f"{self.base_url}{url}", json=data) as response:
                return await response.json()

    async def put(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with ClientSession(headers=self.headers) as session:
            async with session.put(f"{self.base_url}{url}", json=data) as response:
                return await response.json()

    async def delete(self, url: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        async with ClientSession(headers=self.headers) as session:
            async with session.delete(f"{self.base_url}{url}", params=params) as response:
                return await response.json()

    async def html(self, url: str) -> str:
        async with ClientSession(headers=HEADERS) as session:
            async with session.get(f"{self.base_url}{url}") as response:
                return await response.text(encoding="utf-8")

    async def crawl(self, url: str) -> Website:
        html = await self.html(url)
        soup = BeautifulSoup(html, "lxml")
        images = []
        links = []
        for img in soup.find_all("img",src=True):
            if img["src"].startswith("http") and img["src"] not in images:
                images.append(img["src"])
            elif img["src"].startswith("/") and f"{self.base_url}{img['src']}" not in images:
                images.append(f"{self.base_url}{img['src']}")
            else:
                pass
        for link in soup.find_all("a", href=True):
            if link["href"].startswith("http") and link["href"] not in links:
                links.append(link["href"])
            elif link["href"].startswith("/") and link["href"] not in links:
                links.append(f"{self.base_url}{link['href']}")
            else:
                pass
        return Website(
            url=url,
            text=soup.get_text(),
            links=links,
            images=images
        )
    
    async def auth(self, request:Request) -> Dict[str, Any]:
        token = request.headers["Authorization"].split(" ")[1]
        headers = {
            "Authorization": f"Bearer {token}"
        }
        async with ClientSession(headers=headers) as session:
            async with session.get(f"https://{AUTH0_DOMAIN}/userinfo") as response:
                return await response.json()

class App(FastAPI):
    def __init__(self):
        super().__init__()
        self.aws = AWSClient()  
        self.http = APIClient()
        self.mount("/static", StaticFiles(directory="static"), name="static")

            
        @self.post("/api/upload/{sub}")
        async def upload( sub:str,file:UploadFile=File(...))->HttpUrl:
            return await self.aws.upload(sub, file)

        @self.get("/api/upload/{sub}")
        async def list_uploads(sub:str)->List[Dict[str,Any]]:
            return await self.aws.list_uploads(sub)

        @self.delete("/api/upload/{key}")
        async def delete_upload(key:str)->Dict[str,Any]:
            return await self.aws.delete_upload(key)

        @self.post("/api/email")
        async def send_email(sender:EmailStr,subject:str,body:str)->Dict[str,Any]:
            return await self.aws.send_email(sender,subject,body)

        @self.get("/api/translate/{source}/{target}/{text}")
        async def translate(source:str,target:str,text:str)->Dict[str,Any]:
            return await self.aws.translate(text,source,target)

        @self.post("/api/comprehend/{text}")
        async def comprehend(text:str)->Dict[str,Any]:
            return await self.aws.comprehend(text)

        @self.post("/api/rekognition")
        async def rekognition(file:UploadFile=File(...))->Dict[str,Any]:
            return await self.aws.rekognition(file) 

        @self.get("/api/polly/{text}")
        async def polly(text:str)->Dict[str,Any]:
            return await self.aws.polly(text)

        @self.post("/api/transcribe/{sub}/{lang}")
        async def transcribe(sub:str,lang:str="es",file:UploadFile=File(...))->Dict[str,Any]:
            return await self.aws.transcribe(sub,lang,file)
        
        @self.get("/api/syntax/{text}/{lang}")
        async def syntax(text:str,lang:str="es")->Dict[str,Any]:
            return await self.aws.syntax(text,lang)

app = App()
