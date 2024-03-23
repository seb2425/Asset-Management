from model import User,Login
import motor.motor_asyncio

client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database=client.Users
collection=database.users

#CREATE USER
async def create_user(user):
    document=user
    result =await collection.insert_one(document)
    return document

#GET ALL USERS
async def get_users():
    users=[]
    userlist=collection.find({})
    async for u in userlist:
        users.append(Login(**u))
    return users