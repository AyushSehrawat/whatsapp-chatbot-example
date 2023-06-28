from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.routers import whatsapp
from app.utils.constants import MONGO_URL

app = FastAPI()


async def connect_to_mongodb():
    client = AsyncIOMotorClient(MONGO_URL)
    return client


@app.on_event("startup")
async def startup():
    app.mongodb_client = await connect_to_mongodb()
    app.mongodb = app.mongodb_client["notbot"]
    print("[INFO] Connected to MongoDB [notbot]")


@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()
    print("[INFO] Disconnected from MongoDB [notbot]")


app.include_router(whatsapp.router)


@app.get("/")
async def root():
    return {"message": "Welcome to NotBot"}
