import json

from dataclasses import dataclass, field
from enum import StrEnum


class BaseType:
    def to_dict(self) -> dict:
        return {
            k: v.__dict__ if isinstance(v, BaseType) else v for k, v in self.__dict__.items()
        }


class AwemeType(StrEnum):
    VIDEO = "video"
    ALBUM = "album"


aweme_type_codes = {
    0: AwemeType.VIDEO,
    51: AwemeType.VIDEO,
    55: AwemeType.VIDEO,
    58: AwemeType.VIDEO,
    61: AwemeType.VIDEO,
    150: AwemeType.ALBUM,
}


@dataclass
class Statistics:
    comment_count: int
    digg_count: int
    download_count: int
    play_count: int
    share_count: int
    forward_count: int
    lose_count: int
    lose_comment_count: int
    whatsapp_share_count: int
    collect_count: int
    repost_count: int


@dataclass
class Author:
    uid: str
    nickname: str
    unique_id: str
    sec_uid: str


@dataclass
class Video:
    url: str
    weight: int
    height: int


@dataclass
class Image:
    url: str
    height: int
    width: int


@dataclass
class Aweme:
    id: str
    type: AwemeType
    create_time: int
    author: Author
    statistics: Statistics
    video: Video
    description: str
    images: list[Image] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Aweme":
        if image_post_info := data.get("image_post_info"):
            images = [
                Image(
                    url=image["display_image"]["url_list"][0],
                    height=image["display_image"]["height"],
                    width=image["display_image"]["width"],
                )
                for image in image_post_info["images"]
            ]
        else:
            images = []

        aweme_type = aweme_type_codes.get(data["aweme_type"], AwemeType.VIDEO)

        return cls(
            id=data["aweme_id"],
            type=aweme_type,
            create_time=data["create_time"],
            description=data["desc"],
            author=Author(
                uid=data["author"]["uid"],
                nickname=data["author"]["nickname"],
                unique_id=data["author"]["unique_id"],
                sec_uid=data["author"]["sec_uid"],
            ),
            statistics=Statistics(
                comment_count=data["statistics"]["comment_count"],
                digg_count=data["statistics"]["digg_count"],
                download_count=data["statistics"]["download_count"],
                play_count=data["statistics"]["play_count"],
                share_count=data["statistics"]["share_count"],
                forward_count=data["statistics"]["forward_count"],
                lose_count=data["statistics"]["lose_count"],
                lose_comment_count=data["statistics"]["lose_comment_count"],
                whatsapp_share_count=data["statistics"]["whatsapp_share_count"],
                collect_count=data["statistics"]["collect_count"],
                repost_count=data["statistics"]["repost_count"],
            ),
            video=Video(
                url=data["video"]["play_addr"]["url_list"][0],
                weight=data["video"]["width"],
                height=data["video"]["height"],
            ),
            images=images,
        )
