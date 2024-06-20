import uuid
from pathlib import Path

from fastapi import HTTPException

from database.models import Video
from tasks import convert_video_to_mp4


class VideoController:
    def __init__(self, db, id):
        self.db = db
        self.user_id = id

    async def convert_video_mp4(self, file):
        try:
            file_type = file.filename.split(".")[-1]
            file_path = f"video/{uuid.uuid4()}.{file_type}"
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())

            video_name = file.filename
            video_size = Path(file_path).stat().st_size
            video = Video(
                name=video_name,
                video_path=file_path,
                owner_id=self.user_id,
                size=video_size,
                status="uploaded",
            )
            self.db.add(video)
            self.db.commit()

            convert_video_to_mp4.delay(video.id)

            return "video uploaded successfully"

        except Exception as e:
            return HTTPException(
                status_code=500, detail=f"Failed to convert video: {str(e)}"
            )

    def search_Video(self, name, size, status):
        filters = []
        if name:
            filters.append(Video.name.ilike(f"%{name}%"))
        if size:
            filters.append(Video.size == size)
        if status:
            filters.append(Video.status == status)
        search = (
            self.db.query(Video)
            .filter(Video.owner_id == self.user_id)
            .filter(*filters)
            .order_by(Video.id.desc())
            .all()
        )
        return search
