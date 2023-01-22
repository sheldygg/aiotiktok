from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, HttpUrl


class Video(BaseModel):
    video_url: HttpUrl


class Album(BaseModel):
    images_url: List[HttpUrl]


class VideoData(BaseModel):
    status: str
    video_type: str
    media: Union[Video, Album]
    cover: HttpUrl
    dynamic_cover: HttpUrl
    description: str
    play_count: int
    comment_count: int
    download_count: int
    share_count: int
    create_time: datetime
    author_name: str
    author_nick: str
    author_pic: HttpUrl
    music_title: str
    music_author: str
    music_url: HttpUrl
    music_cover: HttpUrl

    class Config:
        smart_union = True
