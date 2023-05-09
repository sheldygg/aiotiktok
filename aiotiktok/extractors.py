import json
import re

from .types import Album, Video, VideoData

video_type_codes = {
    0: "video",
    51: "video",
    55: "video",
    58: "video",
    61: "video",
    150: "album",
}


def extract_video_data(data: dict) -> VideoData:
    video_type_code = data["aweme_type"]
    video_type = video_type_codes.get(video_type_code, "video")
    if video_type == "album":
        images_list = []
        for images in data["image_post_info"]["images"]:
            images_list.append(images["display_image"]["url_list"][0])
        media = Album(images_url=images_list)
    else:
        media = Video(video_url=data["video"]["play_addr"]["url_list"][0])
    return VideoData(
        status="success",
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
        author_name=data["author"]["nickname"],
        author_nick=data["author"]["unique_id"],
        author_pic=data["author"]["avatar_medium"]["url_list"][0],
        music_title=data["music"]["title"],
        music_author=data["music"]["author"],
        music_url=data["music"]["play_url"]["uri"],
        music_cover=data["music"]["cover_large"]["url_list"][0],
    )


def extract_user_feed(data: str):
    pattern = r'<script id="SIGI_STATE" type="application\/json">(.*?)<\/script>'
    match = re.search(pattern, data, re.S)
    return json.loads(match.group(1))
