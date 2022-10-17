"""Fauna DB Wrapper"""
from os import environ
from typing import List, Dict, Any, Callable, Optional
from pydantic import BaseModel, Field, Extra, BaseConfig, create_model
from datetime import datetime
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.errors import FaunaError
from faunadb.objects import Ref
from fastapi import *
from fastapi.responses import *


from dotenv import load_dotenv

load_dotenv()

class FQLClient(FaunaClient):
    """Client for FaunaDB"""
    def __init__(self):
        super().__init__(secret=environ['FAUNA_SECRET'])

class FaunaModel(BaseModel):
    """Wrapper for FaunaDB."""
    class Config(BaseConfig):
        """Customize pydantic model."""
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            object: lambda v: v.__dict__,
            Ref: lambda v: v.id(),
            FaunaError: lambda v: v.description
        }
        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True
        extra = Extra.allow

    @property
    def client(self):
        """Returns a FaunaDB client."""
        return FQLClient().query
    @property
    def collection(self)->str:
        """Returns the collection name."""
        return f"{self.__class__.__name__}".lower() + "s"

    @property
    def indexes(self) -> List[Dict[str, Any]]:
        """Returns a list of indexes."""
        keys = []
        for key in self.__fields__.keys():
            if self.__fields__[key].field_info.extra.get("index"):
                keys.append(key)
        return [{
            "name": f"{self.collection}_by_{key}".lower(),
            "source": self.collection,
            "terms": [{
                "field": ["data", key]
            }]
        } for key in keys]

    def init(self):
        """Initializes a collection and indexes."""
        self.create_collection()
        self.create_indexes()
        return self

    def create_collection(self):
        """Creates a collection."""
        self.client(
            q.if_(
                q.exists(q.collection(self.collection)),
                True,
                q.create_collection(
                    {"name": self.collection})))
        self.client(q.if_(
            q.exists(q.index(f"{self.collection}_all")),
            True,
            q.create_index(
                {"name": f"{self.collection}_all",
                "source": q.collection(self.collection)})))
        return self

    def create_indexes(self):
        """Creates indexes for a collection."""
        for index in self.indexes:
                self.client(
                    q.if_(
                        q.exists(q.index(index["name"])),
                        True,
                        q.create_index({
                            "name": index["name"],
                            "source": q.collection(index["source"]),
                            "terms": index["terms"]
                        })))
                return self

    def put(self):
        """Creates a document."""
        return self.client(q.create(q.collection(self.collection), {"data": self.dict()}))

    def get(self):
        """Gets a document."""
        for index in self.indexes:
            try:
                return self.client(q.get(q.match(q.index(index["name"]), 
                self.dict()[index["terms"][0]["field"][1]])))
            except FaunaError as error:
                raise error

    def update(self, data):
        """Updates a document."""
        for index in self.indexes:
            try:
                return self.client(q.update(q.select("ref", q.get(q.match
                (q.index(index["name"]), self.dict()
                [index["terms"][0]["field"][1]]))), {"data": data}))
            except FaunaError as error:
                raise error

    def delete(self):
        """Deletes a document."""
        for index in self.indexes:
            try:
                return self.client(q.delete(q.select("ref", q.get(q.match(q.index(index["name"]), self.dict()[index["terms"][0]["field"][1]])))))
            except FaunaError as error:
                raise error

    def scan(self):
        """Returns all document records in a collection."""
        return self.client(q.paginate(q.match(q.index(f"{self.collection}_all".lower()))))

    def all(self):
        """Returns all document refs"""
        return self.client(q.map_(lambda ref: q.get(ref), self.scan()))

    def sort(self, key:str,reverse:bool=False)->List[Dict[str, Any]]:
        """Sorts a table scan by a key."""
        return sorted(self.all(), key=lambda x: x["data"][key], reverse=reverse)

    def filter(self, key:str, value:Any)->List[Dict[str, Any]]:
        """Filters a table scan by a key and value."""
        return list(filter(lambda x: x["data"][key] == value, self.all()))

    def paginate(self, size:int=10, after:Ref=None, before:Ref=None):
        """Paginates a table scan."""
        return self.client(q.paginate(q.match(q.index(f"{self.collection}_all".lower())), size=size, after=after, before=before))

class Module:
    """Encapsulates a CRUD module."""
    controller:APIRouter
    model:FaunaModel
    dependencies:Optional[List[Depends]] = None
    service:Optional[Callable] = None

    def __init__(self, controller:APIRouter, model:FaunaModel, dependencies:Optional[List[Depends]]=None):
        self.controller = controller if controller else APIRouter(prefix=f"/{model.collection}", tags=[model.collection], dependencies=dependencies)
        self.model = model
        self.dependencies = dependencies
        self.model.init()

        @self.controller.post("/", dependencies=self.dependencies)
        def create_endpoint(model:FaunaModel=Depends(self.model)):
            """Creates a document."""
            return model.put()

        @self.controller.get("/", dependencies=self.dependencies)
        def get_endpoint(model:FaunaModel=Depends(self.model)):
            """Gets a document."""
            return model.get()

        @self.controller.put("/", dependencies=self.dependencies)
        def update_endpoint(data:Dict[str, Any], model:FaunaModel=Depends(self.model)):
            """Updates a document."""
            return model.update(data)

        @self.controller.delete("/", dependencies=self.dependencies)
        def delete_endpoint(model:FaunaModel=Depends(self.model)):
            """Deletes a document."""
            return model.delete()

        @self.controller.get("/all", dependencies=self.dependencies)
        def get_all_endpoint(model:FaunaModel=Depends(self.model)):
            """Returns all document refs."""
            return model.all()

        @self.controller.get("/sort", dependencies=self.dependencies)
        def sort_endpoint(key:str, reverse:bool=False, model:FaunaModel=Depends(self.model)):
            """Sorts a table scan by a key."""
            return model.sort(key, reverse)

        @self.controller.get("/filter", dependencies=self.dependencies)
        def filter_endpoint(key:str, value:Any, model:FaunaModel=Depends(self.model)):
            """Filters a table scan by a key and value."""
            return model.filter(key, value)

        @self.controller.get("/paginate", dependencies=self.dependencies)
        def paginate_endpoint(size:int=10, after:Ref=None, before:Ref=None, model:FaunaModel=Depends(self.model)):
            """Paginates a table scan."""
            return model.paginate(size, after, before)

class App(FastAPI):
    """Encapsulates a CRUD app."""
    def __init__(self, *args, modules:List[Optional[Module]]=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules = modules
        if self.modules:
            for module in self.modules:
                self.include_router(module.controller)

class User(FaunaModel):
    """Encapsulates a user model."""
    ... # omitted for brevity
