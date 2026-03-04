from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

# Module-level client and db references, populated on startup
client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def connect_to_mongo() -> None:
    """Create the Motor client and wire up the module-level db reference."""
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    # Ping to verify the connection is reachable
    await client.admin.command("ping")
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")


async def close_mongo_connection() -> None:
    """Close the Motor client on shutdown."""
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """Return the current database instance.

    Raises RuntimeError if called before connect_to_mongo() has run.
    """
    if db is None:
        raise RuntimeError(
            "Database not initialised. "
            "Call connect_to_mongo() before using get_database()."
        )
    return db
