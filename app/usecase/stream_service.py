from app.domain.stream import Stream, StreamRepository
from datetime import datetime


class StreamService:
    def __init__(self, repo: StreamRepository):
        self.repo = repo

    async def create_stream(self, title: str, description: str = "") -> Stream:
        stream = Stream(
            id=None,
            title=title,
            description=description,
            is_live=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return await self.repo.create(stream)

    async def get_stream(self, stream_id: str):
        return await self.repo.get_by_id(stream_id)

    async def list_streams(self):
        return await self.repo.list_all()

    async def update_stream(self, stream_id: str, data: dict):
        data["updated_at"] = datetime.utcnow()
        return await self.repo.update(stream_id, data)

    async def delete_stream(self, stream_id: str):
        return await self.repo.delete(stream_id)
