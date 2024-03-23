from pydantic import BaseModel,Field,EmailStr
from typing import Optional
class Asset(BaseModel):
    id:int
    name:str
    type:str
    location:str
    buy_d:int
    icost:int
    opstat:str

class UpdateAsset(BaseModel):
    attribute:str
    new_value:str

class AssetPerformance(BaseModel):
    id:int
    uptime:int=Field(default=None)
    downtime:int=Field(default=None)
    maintainence:int=Field(default=None)
    failure_rate:int=Field(default=None)
    efficiency:int=Field(default=None)
    class Config:
        schema={
            "user_demo": {
                "id":0,
                "uptime": 10,
                "downtime": 5,
                "maintenance": 2,
                "failure_rate": 3,
                "efficiency": 90
            }
        }


class User(BaseModel): 
    fullname:str=Field(default=None)
    email:EmailStr=Field(default=None)
    password:str=Field(default=None)
    class Config:
        schema={
            "user_demo":{
                "fullname":"ateeb",
                "email":"jj@x.com",
                "password":"password"
            }
        }
    

class Login(BaseModel):
    email:EmailStr=Field(default=None)
    password:str=Field(default=None)
    class Config:
        schema={
            "user_demo":{
                "email":"jj@x.com",
                "password":"password"
            }
        }
    

