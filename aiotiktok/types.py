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


class Video(Struct):
    url: str


class Album(Struct):
    urls: list[str]


class Author(Struct, kw_only=True):
    id: str
    unique_id: str
    nickname: str
    sec_uid: str | None = None
    avatar: str


class Music(Struct):
    title: str
    author: str
    url: str
    cover: str


class VideoData(Struct):
    video_type: VideoType
    media: Video | Album
    cover: str
    dynamic_cover: str
    description: str
    play_count: int
    comment_count: int
    download_count: int
    share_count: int
    create_time: datetime
    author: Author
    music: Music
