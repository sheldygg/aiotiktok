import re

from aiohttp import ClientSession
from .types import Video, Album, VideoData
from .exceptions import URLUnavailable, VideoUnavailable


class Client:
    def __init__(self) -> None:
        self.tiktok_api_headers = {
            "user-agent": "com.ss.android.ugc.trill/2613 (Linux; U; Android 10; en_US; Pixel 4; "
                          "Build/QQ3A.200805.001; Cronet/58.0.2991.0)"
        }
        self.tiktok_url = "https://www.tiktok.com/"
        self.tiktok_api_url = (
            "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={}"
        )
        self.video_type_codes = {
            0: "video",
            51: "video",
            55: "video",
            58: "video",
            61: "video",
            150: "album",
        }

    async def get_video_id(self, url: str):
        if "@" in url:
            pass
        else:
            async with ClientSession() as session:
                async with session.get(url=url, allow_redirects=False) as resp:
                    url = resp.headers["Location"].split("?")[0]
        if url == self.tiktok_url or "video" not in url:
            raise URLUnavailable("URLUnavailable, check the link")
        video_id = re.findall("/video/(\d+)?", url)[0]
        return video_id

    async def request(self, url: str):
        async with ClientSession() as session:
            async with session.get(url, headers=self.tiktok_api_headers) as resp:
                response = (await resp.json())["aweme_list"][0]
        return response

    def extract_video_data(self, data):
        video_type_code = data["aweme_type"]
        video_type = self.video_type_codes.get(video_type_code, "video")
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

    async def get_data(self, url: str):
        """
        Get TikTok data
        :param url: url to video
        :return: dict
        """
        video_id = await self.get_video_id(url)
        tiktok_api_link = self.tiktok_api_url.format(video_id)
        data = await self.request(tiktok_api_link)
        if data and data["aweme_id"] == video_id:
            return self.extract_video_data(data)
        raise VideoUnavailable("VideoUnavailable")
