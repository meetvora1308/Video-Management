import uuid

from moviepy.editor import VideoFileClip

from database.database import SessionLocal
from database.models import Video
from celery_config import app


@app.task
def convert_video_to_mp4(video_id):
    try:
        db = SessionLocal()
        video_record = db.query(Video).filter(Video.id == video_id).first()

        input_path = video_record.video_path
        output_path = f"uploads/{uuid.uuid4()}.mp4"

        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path)

        # Update the video record with the new file path
        video_record.file_path = output_path
        video_record.status = "converted"
        db.commit()
        db.close()
    except Exception as e:
        raise Exception(f"Failed to convert video: {str(e)}")
