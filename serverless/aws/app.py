from typing import *
from pydantic import *
from fastapi import *
from fastapi.responses import *
from aioboto3 import Session
from aiohttp import ClientSession
from boto3 import Session as Boto3Session
from os import environ
from dotenv import load_dotenv
from typer import Typer
load_dotenv()

AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION = environ['AWS_DEFAULT_REGION']
AWS_SES_EMAIL = environ['AWS_SES_EMAIL']
AWS_S3_BUCKET = environ['AWS_S3_BUCKET']

class Service(Session):
    """User Session for AWS."""
    def __init__(self):
        credentials = Boto3Session().client('sts').get_session_token()['Credentials']
        super().__init__(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=AWS_DEFAULT_REGION
        )

class Controller(APIRouter):
    """Base Controller class for all controllers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class Module(FastAPI):
    """Base Module class for all modules."""
    def __init__(self, service:Service, controller:Controller, *args, **kwargs):
        self.service = service
        self.controller = controller
        super().__init__(*args, **kwargs)
        self.include_router(self.controller)
        
