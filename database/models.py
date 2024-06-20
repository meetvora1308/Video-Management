from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    create_engine,
    Enum,
)
from sqlalchemy.orm import declarative_base, relationship
import enum


SQLALCHEMY_DATABASE_URL = "sqlite:///./actual.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
metadata = MetaData()


class VideoStatus(enum.Enum):
    uploaded = "uploaded"
    converted = "converted"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    videos = relationship("Video", back_populates="owner")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    video_path = Column(String)
    file_path = Column(String)
    size = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(VideoStatus), default=VideoStatus.uploaded)

    owner = relationship("User", back_populates="videos")
