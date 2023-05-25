from datetime import datetime
from enum import Enum

from msgspec import Struct


class VideoType(str, Enum):
    VIDEO = "video"
    ALBUM = "album"


video_type_codes = {
    0: VideoType.VIDEO,
    51: VideoType.VIDEO,
    55: VideoType.VIDEO,
    58: VideoType.VIDEO,
    61: VideoType.VIDEO,
    150: VideoType.ALBUM,
}


class Video(Struct, array_like=True):
    url: str


class Album(Struct, array_like=True):
    urls: list[str]


class Author(Struct, array_like=True):
    unique_id: str
    nickname: str
    avatar: str
    id: str | None = None
    sec_uid: str | None = None


class Music(Struct, array_like=True):
    title: str
    author: str
    url: str
    cover: str


class Statistics(Struct, array_like=True):
    likes: int
    plays: int
    comments: int
    downloads: int
    shares: int
    saves: int


class VideoData(Struct, array_like=True):
    url: str
    video_type: VideoType
    media: Video | Album | None
    cover: str
    dynamic_cover: str
    description: str
    statistics: Statistics
    create_time: datetime
    author: Author
    music: Music
