import json
import re

from .types import Album, Author, Video, VideoData, VideoType, video_type_codes


def extract_video_data(data: dict) -> VideoData:
    video_type = video_type_codes.get(data["aweme_type"], VideoType.VIDEO)
    if video_type == VideoType.ALBUM:
        images_list = []
        for images in data["image_post_info"]["images"]:
            images_list.append(images["display_image"]["url_list"][0])
        media = Album(urls=images_list)
    else:
        media = Video(url=data["video"]["play_addr"]["url_list"][0])
    author_data = data.get("author")
    author = Author(
        id=author_data.get("id"),
        nickname=author_data.get("nickname"),
        unique_id=author_data.get("unique_id"),
        avatar=author_data.get("avatar_larger", {}).get("url_list")[0],
    )
    return VideoData(
        video_type=video_type,
        media=media,
        cover=data["video"]["cover"]["url_list"][0],
        dynamic_cover=data["video"]["dynamic_cover"]["url_list"][0],
        description=data["desc"],
        play_count=data["statistics"]["comment_count"],
        comment_count=data["statistics"]["comment_count"],
        download_count=data["statistics"]["download_count"],
        share_count=data["statistics"]["share_count"],
        create_time=data["create_time"],
        author=author,
        music_title=data["music"]["title"],
        music_author=data["music"]["author"],
        music_url=data["music"]["play_url"]["uri"],
        music_cover=data["music"]["cover_large"]["url_list"][0],
    )


def extract_data_from_html(data: str):
    pattern = r'<script id="SIGI_STATE" type="application\/json">(.*?)<\/script>'
    match = re.search(pattern, data, re.S)
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
