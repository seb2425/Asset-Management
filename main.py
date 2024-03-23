from fastapi import FastAPI,HTTPException,status,Query,Body,dependencies,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model import Asset,UpdateAsset,User,Login,AssetPerformance
from auth.jwt_handler import encode_jwt
from auth.jwt_bearer import jwtBearer


from database import(
    fetch_one_asset,
    fetch_all,
    create_asset,
    update_asset,
    delete_asset
)

from database2 import(
    create_user,
    get_users
)

from database3 import(
    fetch_one_assetp,
    fetch_allp,
    create_assetp,
    update_assetp,
    delete_assetp
)

app=FastAPI()


my_assets=[]

origins=["https://localhost:3000"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
)


#*********************ASSET SECTION******************************************

#Helper functions
def find_assset_id(id):
    for i,p in enumerate(my_assets):
         if p and p.get('id')==id: #p needs to be a dict
            return i
    return None

#CREATE
@app.post("/asset",response_model=Asset,dependencies=[Depends(jwtBearer())])
async def casset(asset:Asset):
    asset=asset.dict()
    result=await create_asset(asset)
    if(result):
        return result
    raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="couldn't create asset"))

#READ
@app.get("/asset")
async def read():
    response =await fetch_all()
    return response

#READ ONE
@app.get("/asset/{id}",response_model=Asset)
async def get_one_asset(id:int):
    response =await fetch_one_asset(id)
    if(response):
        return response
    raise(HTTPException(status.HTTP_404_NOT_FOUND,detail="not found"))


#UPDATE
@app.put("/asset/{id}",response_model=Asset)
async def upd(id:int,upd:UpdateAsset):
    attribute=upd.attribute
    new_value=upd.new_value
    if(attribute not in ['name', 'type', 'location', 'buy_d', 'icost', 'opstat']):
        raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="invalid attribute"))
    
    result =await update_asset(id,attribute,new_value)
    if(result):
        return result
    raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="couldn't update asset"))


#DELETE
@app.delete("/asset/{id}")
async def del_asset(id:int):
    result =await delete_asset(id)
    if(result):
        raise(HTTPException(status.HTTP_204_NO_CONTENT,detail="deleted asset"))
    raise(HTTPException(status.HTTP_404_NOT_FOUND,detail="could not find asset"))

#*********************END OF ASSET SECTION******************************************

#*******************************USER SECTION************************************************#
#SIGNUP user
#users=[]
@app.post("/user/signup")
async def singup(user:User):
    user=user.model_dump()
    result= await create_user(user)
    if(result):
        raise(HTTPException(status.HTTP_200_OK,detail="user added"))
    raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="could not create user"))
    #users.append(user)
    #return encode_jwt(user.email)

#CHECK USER
async def check_user(data:Login):
    users=await get_users()
    for user in users:
        if user.email==data.email and user.password==data.password:
            return True
    return False

async def check_user_exists(userID: str):
        users=await get_users()
        for user in users:
            if user.email == userID:  # Assuming the email is used as the userID
                return True
        return False

#USER LOGIN
@app.post("/user/login")
async def login(user:Login):
    if await check_user(user):
        return encode_jwt(user.email)
    else:
        return "invalid login details"
    
#*************************************END OF USER SECTION*******************************************************#
    

#************************************ASSET PERFORMANCE SECTION*******************************************#
#Get all performance 
@app.get("/asset/perform/all")
async def get_perm():
    data= await fetch_allp()
    return data

@app.get("/asset/perform/{id}" ,response_model=AssetPerformance)
async def get_one_perm(id:int):
    data= await fetch_one_assetp(id)
    if(data):
        return data
    raise(HTTPException(status.HTTP_404_NOT_FOUND,detail="not found"))

@app.post("/asset/perform/",response_model=AssetPerformance)
async def create_perm(per:AssetPerformance):
    per=per.model_dump()
    result =await create_assetp(per)
    if(result):
        return result
    raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="couldn't create asset"))

@app.put("/asset/performance/{id}",response_model=AssetPerformance)
async def update_perm(id:int,upd:UpdateAsset):
    attribute=upd.attribute
    value=upd.new_value
    if (attribute not in ['uptime','downtime','maintainence','failure_rate','efficiency']):
        raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="invalid attribute"))
    result=await update_assetp(id,attribute,value)
    if(result):
        return result
    raise(HTTPException(status.HTTP_400_BAD_REQUEST,detail="couldn't update asset"))

@app.delete("/asset/performance/{id}")
async def del_perm(id:int):
    result =await delete_assetp(id)
    if(result):
        raise(HTTPException(status.HTTP_204_NO_CONTENT,detail="deleted"))
    raise(HTTPException(status.HTTP_404_NOT_FOUND,detail="could not find asset"))

#*****************************END OF ASSET PERFORMANCE SECTION***************************************#

#*****************************ASSET PERFORMANCE FUNCTIONS*************************#

#GET AVERAGE DOWNTIME
@app.get("/asset/downtime/avg")
async def get_avg_d():
    get_assets=await fetch_allp()
    count=0
    sum=0
    for asset in get_assets:
        count+=1
        sum+=asset.downtime
    av=sum/count
    return {"average downtime is":av}

#GET TOTAL MAINTAINENCE COST
@app.get("/asset/maintainence/total")
async def total_maintainence_cost():
    get_assets=await fetch_allp()
    total=0
    for asset in get_assets:
        total+=asset.maintainence
    return {"total maintaincene cost is":total}

#GET ASSET WITH HIGHESTFAILURE RATE
@app.get("/asset/failure/highest")
async def highest_failure():
    get_assets=await fetch_allp()
    fail_id=-1
    fail_rate=0
    for asset in get_assets:
        if(asset.failure_rate>fail_rate):
            fail_id=asset.id
            fail_rate=asset.failure_rate
    return {"the asset with hgihest failure rate has id":fail_id}

#GET ASSET WITH ABOVE THRESHOLD FAILURE RATE
@app.get("/asset/failure/high/{threshold}")
async def high_fail_rates(threshold:int):
    get_assets=await fetch_allp()
    #fail_threshold=50 #set this to any value,above of which we will consider high failure rate
    failures=[]
    for asset in get_assets:
        if(asset.failure_rate>threshold):
            failures.append(asset.model_dump())
    return failures