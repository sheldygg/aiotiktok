import re

from aiohttp import ClientSession

from .exceptions import URLUnavailable, VideoUnavailable


class Tiktok:
    def __init__(self) -> None:
        self.tiktok_api_headers = {
            "user-agent": "com.ss.android.ugc.trill/2613 (Linux; U; Android 10; en_US; Pixel 4; Build/QQ3A.200805.001; Cronet/58.0.2991.0)"
        }
        self.tiktok_url = "https://www.tiktok.com/"
        self.tiktok_api_url = "https://api-h2.tiktokv.com/aweme/v1/feed/?aweme_id={}&version_code=2613&aid=1180"

    async def get_video_id(self, original_url: str):
        if "@" in original_url:
            return original_url
        else:
            async with ClientSession() as session:
                async with session.get(url=original_url, allow_redirects=False) as resp:
                    original_url = resp.headers["Location"].split("?")[0]
        return original_url

    async def tiktok(self, original_url: str):
        """
        Get TikTok data
        :param original_url: url to video
        :return: dict
        """

        original_url = await self.get_video_id(original_url)
        if original_url == self.tiktok_url or "video" not in original_url:
            raise URLUnavailable("URLUnavailable, check the link")
        else:
            video_id = re.findall("/video/(\d+)?", original_url)[0]
        tiktok_api_link = self.tiktok_api_url.format(video_id)

        async with ClientSession() as session:
            async with session.get(
                url=tiktok_api_link, headers=self.tiktok_api_headers
            ) as response:
                predata = await response.json()
        if predata:
            data = predata["aweme_list"][0]
            if data["aweme_id"] == video_id:
                if "image_post_info" in data:
                    video_type = "album"
                    media = []
                    for images in data["image_post_info"]["images"]:
                        media.append(images["display_image"]["url_list"][0])
                else:
                    video_type = "video"
                    media = data["video"]["play_addr"]["url_list"][0]
                return dict(
                    status="success",
                    video_type=video_type,
                    media=media,
                    cover=data["video"]["cover"]["url_list"][0],
                    dynamic_cover=data["video"]["dynamic_cover"]["url_list"][0],
                    desc=data["desc"],
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
            else:
                raise VideoUnavailable("VideoUnavailable")
        return
