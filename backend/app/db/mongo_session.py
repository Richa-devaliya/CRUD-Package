# backend/app/db/mongo_session.py
import motor.motor_asyncio
from app.core.config import settings

class MongoSessionManager:
    """
    Manages the connection and session to the MongoDB database.
    """
    def __init__(self):
        self.client = None
        self.db = None

    async def init_db(self):
        """
        Initializes the MongoDB client and database instance.
        """
        if settings.DB_TYPE == "mongo":
            self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB]

    async def close_db(self):
        """
        Closes the MongoDB client connection.
        """
        if self.client:
            self.client.close()

    def get_db(self):
        """
        Returns the database instance.
        """
        if self.db is None:
            raise Exception("MongoDB not initialized. Call init_db() first.")
        return self.db

mongo_session = MongoSessionManager()