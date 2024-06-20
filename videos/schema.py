from pydantic import BaseModel


class VideoCreate(BaseModel):
    name: str
    size: int
    file: bytes


class SearchVideo(BaseModel):
    search: str
