from app.domain.stream import Stream, StreamRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


class MongoStreamRepository(StreamRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["streams"]

    def _doc_to_stream(self, doc) -> Stream:
        return Stream(
            id=str(doc["_id"]),
            title=doc["title"],
            description=doc.get("description"),
            is_live=doc["is_live"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )

    async def create(self, stream: Stream) -> Stream:
        doc = stream.__dict__.copy()
        doc.pop("id", None)
        result = await self.collection.insert_one(doc)
        stream.id = str(result.inserted_id)
        return stream

    async def get_by_id(self, stream_id: str):
        doc = await self.collection.find_one({"_id": ObjectId(stream_id)})
        return self._doc_to_stream(doc) if doc else None

    async def list_all(self):
        streams = []
        async for doc in self.collection.find().sort("created_at", -1):
            streams.append(self._doc_to_stream(doc))
        return streams

    async def update(self, stream_id: str, data: dict):
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(stream_id)},
            {"$set": data},
            return_document=True,
        )
        return self._doc_to_stream(result) if result else None

    async def delete(self, stream_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(stream_id)})
        return result.deleted_count > 0
