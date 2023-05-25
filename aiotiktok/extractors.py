import json
import re

from .types import (
    Album,
    Author,
    Music,
    Statistics,
    Video,
    VideoData,
    VideoType,
    video_type_codes,
)


def create_url_to_video(username: str, video_id: str):
    return f"https://www.tiktok.com/@{username}/video/{video_id}"


def extract_video_data(data: dict) -> VideoData:
    video_type = video_type_codes.get(data["aweme_type"], VideoType.VIDEO)
    if video_type == VideoType.ALBUM:
        media = Album(
            urls=[
                images["display_image"]["url_list"][0]
                for images in data["image_post_info"]["images"]
            ]
        )
    elif video_type == VideoType.VIDEO:
        media = Video(url=data["video"]["play_addr"]["url_list"][0])
    else:
        media = None
    author_data = data.get("author", {})
    author = Author(
        id=author_data.get("id"),
        nickname=author_data.get("nickname"),
        unique_id=author_data.get("unique_id"),
        avatar=author_data.get("avatar_larger", {}).get("url_list")[0],
        sec_uid=author_data.get("sec_uid"),
    )
    statistics = data.get("statistics", {})
    return VideoData(
        url=create_url_to_video(author.unique_id, data.get("aweme_id", "")),
        video_type=video_type,
        media=media,
        cover=data["video"]["cover"]["url_list"][0],
        dynamic_cover=data["video"]["dynamic_cover"]["url_list"][0],
        description=data["desc"],
        statistics=Statistics(
            likes=statistics.get("digg_count"),
            plays=statistics.get("play_count"),
            comments=statistics.get("comment_count"),
            downloads=statistics.get("download_count"),
            shares=statistics.get("share_count"),
            saves=statistics.get("collect_count"),
        ),
        create_time=data["create_time"],
        author=author,
        music=Music(
            title=data["music"]["title"],
            author=data["music"]["author"],
            url=data["music"]["play_url"]["uri"],
            cover=data["music"]["cover_large"]["url_list"][0],
        ),
    )


def extract_data_from_html(data: str):
    pattern = r'<script id="SIGI_STATE" type="application\/json">(.*?)<\/script>'
    match = re.search(pattern, data, re.S)
    if match:
        return json.loads(match.group(1))


def extract_user_data(data: dict):
    user_data = list(data.get("UserModule", {}).get("users", {}).values())[0]
    return Author(
        id=user_data.get("id"),
        unique_id=user_data.get("uniqueId"),
        nickname=user_data.get("nickname"),
        sec_uid=user_data.get("secUid"),
        avatar=user_data.get("avatarLarger"),
    )
