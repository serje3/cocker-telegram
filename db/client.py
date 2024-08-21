import os

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.getenv('MONGO_CONNECTION_URL'), authSource='telegram')
db = client['telegram']
