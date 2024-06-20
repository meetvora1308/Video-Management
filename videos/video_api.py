from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import database
from database.models import VideoStatus
from users.auth import get_current_user
from videos.controller import VideoController

router = APIRouter()


@router.post(
    "/upload_video",
)
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_user),
):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a video")
    data = await VideoController(db, token.id).convert_video_mp4(file)
    if isinstance(data, HTTPException):
        return data
    return {"message": data}


@router.get("/search_video")
def search(
    name: Optional[str] = None,
    size: Optional[int] = None,
    db: Session = Depends(database.get_db),
    status: Optional[VideoStatus] = None,
    token: str = Depends(get_current_user),
):
    data = VideoController(db, token.id).search_Video(name, size, status)
    return data
