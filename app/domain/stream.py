from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Stream:
    id: Optional[str]
    title: str
    description: Optional[str]
    is_live: bool
    created_at: datetime
    updated_at: datetime


class StreamRepository:
    async def create(self, stream: Stream) -> Stream:
        raise NotImplementedError

    async def get_by_id(self, stream_id: str) -> Optional[Stream]:
        raise NotImplementedError

    async def list_all(self) -> list[Stream]:
        raise NotImplementedError

    async def update(self, stream_id: str, data: dict) -> Optional[Stream]:
        raise NotImplementedError

    async def delete(self, stream_id: str) -> bool:
        raise NotImplementedError
