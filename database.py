from model import Asset,UpdateAsset
import motor.motor_asyncio

client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database=client.Assets
collection=database.land


#GET ONE
async def fetch_one_asset(id):
    document=await collection.find_one({"id":id})
    return document

#GET ALL
async def fetch_all():
    document=[]
    doclist= collection.find({})
    async for d in doclist:
        document.append(Asset(**d))
    return document

#CREATE
async def create_asset(asset):
    document=asset
    result =await collection.insert_one(document)
    return document

#UPDATE
async def update_asset(id ,attribute, new_value):
    await collection.update_one({"id":id},{"$set":{attribute:new_value}} )
    document =await collection.find_one({"id":id})
    return document

#DELETE
async def delete_asset(id):
    await collection.delete_one({"id":id})
    return True