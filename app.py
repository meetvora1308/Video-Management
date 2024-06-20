from fastapi import FastAPI

from database import database, models
from users import user_api
from videos import video_api


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


app.include_router(user_api.router, tags=["Users"], prefix="/user")
app.include_router(video_api.router, tags=["videos"], prefix="/video")
