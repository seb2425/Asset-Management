from model import AssetPerformance
import motor.motor_asyncio

client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database=client.Asset
collection=database.performance


#GET ONE
async def fetch_one_assetp(id):
    document=await collection.find_one({"id":id})
    return document

#GET ALL
async def fetch_allp():
    document=[]
    doclist= collection.find({})
    async for d in doclist:
        document.append(AssetPerformance(**d))
    return document

#CREATE
async def create_assetp(asset):
    document=asset
    result =await collection.insert_one(document)
    return document

#UPDATE
async def update_assetp(id ,attribute, new_value):
    await collection.update_one({"id":id},{"$set":{attribute:new_value}} )
    document =await collection.find_one({"id":id})
    return document

#DELETE
async def delete_assetp(id):
    await collection.delete_one({"id":id})
    return True