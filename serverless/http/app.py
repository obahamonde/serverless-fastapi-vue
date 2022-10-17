from typing import *
from pydantic import *
from fastapi import *
from fastapi.responses import *
from aiohttp import *
from os import environ
from dotenv import load_dotenv
load_dotenv()

class APIClient:
    """API Client"""
    base_url:Union[str, AnyHttpUrl] = "https://api.github.com/"
    headers:Dict[str,str] = {"Authorization": f"token {environ.get('API_TOKEN')}"}

    async def get(self, endpoint:str) -> Dict[str,Any]:
        """Get Method override"""
        async with ClientSession() as session:
            async with session.get(self.base_url+endpoint, headers=self.headers) as response:
                return await response.json()
            
    async def post(self, endpoint:str, data:Dict[str,Any]) -> Dict[str,Any]:
        """Post Method override"""
        async with ClientSession() as session:
            async with session.post(self.base_url+endpoint, headers=self.headers, json=data) as response:
                return await response.json()
            
    async def patch(self, endpoint:str, data:Dict[str,Any]) -> Dict[str,Any]:
        """Patch Method override"""
        async with ClientSession() as session:
            async with session.patch(self.base_url+endpoint, headers=self.headers, json=data) as response:
                return await response.json()
            
    async def delete(self, endpoint:str) -> Dict[str,Any]:
        """Delete Method override"""
        async with ClientSession() as session:
            async with session.delete(self.base_url+endpoint, headers=self.headers) as response:
                return await response.json()
            
    async def text(self, endpoint:str) -> str:
        """Get text"""
        async with ClientSession() as session:
            async with session.get(self.base_url+endpoint, headers=self.headers) as response:
                return await response.text(encoding="utf-8")

    async def blob(self, endpoint:str) -> bytes:
        """Get blob"""
        async with ClientSession() as session:
            async with session.get(self.base_url+endpoint, headers=self.headers) as response:
                return await response.read()


