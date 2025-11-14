from fastapi import APIRouter, Depends, HTTPException, status
from app.usecase.stream_service import StreamService
from app.domain.stream import Stream
from typing import List
from app.di import get_stream_service
from app.usecase.auth_service import AuthService

router = APIRouter(prefix="/streams", tags=["Streams"])


@router.post("/", response_model=Stream)
async def create_stream(
    title: str,
    description: str = "",
    service: StreamService = Depends(get_stream_service),
    user = Depends(AuthService.get_current_user)
):
    return await service.create_stream(title, description)


@router.get("/", response_model=List[Stream])
async def list_streams(service: StreamService = Depends(get_stream_service), user = Depends(AuthService.get_current_user)):
    return await service.list_streams()


@router.get("/{stream_id}", response_model=Stream)
async def get_stream(stream_id: str, service: StreamService = Depends(get_stream_service), user = Depends(AuthService.get_current_user)):
    stream = await service.get_stream(stream_id)
    if not stream:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")
    return stream


@router.put("/{stream_id}", response_model=Stream)
async def update_stream(
    stream_id: str, data: dict, service: StreamService = Depends(get_stream_service),
    user = Depends(AuthService.get_current_user)
):
    updated = await service.update_stream(stream_id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")
    return updated


@router.delete("/{stream_id}")
async def delete_stream(stream_id: str, service: StreamService = Depends(get_stream_service), user = Depends(AuthService.get_current_user)):
    deleted = await service.delete_stream(stream_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")
    return {"ok": True, "deleted": stream_id}
