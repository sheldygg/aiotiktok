from datetime import datetime
from enum import Enum

from msgspec import Struct
from msgspec.structs import asdict


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

    def dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class Album(Struct, array_like=True):
    urls: list[str]

    def dict(self):
        return asdict(self)


class Author(Struct, array_like=True):
    unique_id: str
    nickname: str
    avatar: str
    id: str | None = None
    sec_uid: str | None = None

    def dict(self):
        return asdict(self)


class Music(Struct, array_like=True):
    id: str
    title: str
    author: str
    url: str
    cover: str

    def dict(self):
        return asdict(self)


class Statistics(Struct, array_like=True):
    likes: int
    plays: int
    comments: int
    downloads: int
    shares: int
    saves: int

    def dict(self):
        return asdict(self)


class VideoData(Struct, array_like=True):
    url: str
    video_type: VideoType
    media: Album | Video | None
    cover: str
    dynamic_cover: str
    description: str
    statistics: Statistics
    create_time: datetime
    author: Author
    music: Music

    def dict(self):
        result_dict = {}
        for field in self.__struct_fields__:
            attr = getattr(self, field)
            if hasattr(attr, "__struct_fields__"):
                result_dict.update({field: attr.dict()})
            else:
                result_dict.update({field: attr})
        return result_dict
