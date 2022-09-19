import re

from aiohttp import ClientSession

from .exceptions import VideoUnavailable, URLUnavailable

class Tiktok():
    def __init__(self) -> None:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }
        self.tiktok_api_link = "https://api-h2.tiktokv.com/aweme/v1/feed/?version_code=2613&aweme_id={}&device_type=Pixel%204"
        self.tiktok_url = "https://www.tiktok.com/"
        
    async def make_session(self):
        self.session = ClientSession()

    async def get_video_id(self, original_url: str):
        if "@" in original_url:
            return original_url
        else:
            await self.make_session()
            resp = await self.session.get(url=original_url, allow_redirects=False)
            original_url = resp.headers["Location"].split("?")[0]
            await self.session.close()
        return original_url

    async def tiktok(self, original_url: str):
        """
        Get TikTok data
        :param original_url: url to video
        :return: dict
        """
        
        original_url = await self.get_video_id(original_url)
        if original_url == self.tiktok_url:
            raise URLUnavailable("URLUnavailable, check the link")
        else:
            video_id = re.findall('/video/(\d+)?', original_url)[0]
        
        await self.make_session()
        response = await self.session.get(self.tiktok_api_link.format(video_id), headers=self.headers)
        predata = await response.json()
        await self.session.close()
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
            
            video_info = {"status": "success",
                        "video_type": video_type,
                        "media": media,
                        "cover": data['video']['cover']['url_list'][0],
                        "dynamic_cover": data['video']['dynamic_cover']['url_list'][0],
                        "desc": data["desc"],
                        "play_count": data["statistics"]["play_count"],
                        "comment_count": data["statistics"]["comment_count"],
                        "download_count": data["statistics"]["download_count"],
                        "share_count": data["statistics"]["share_count"],
                        "create_time": data["create_time"],
                        "author_name": data["author"]["nickname"],
                        "author_nick": data["author"]["unique_id"],
                        "author_pic": data["author"]["avatar_medium"]["url_list"][0],
                        "music_title": data['music']['title'],
                        "music_author": data['music']['author'],
                        "music_url": data['music']['play_url']['uri'],
                        "music_cover": data["music"]["cover_large"]["url_list"][0]
            }
            return video_info
        else:
            raise VideoUnavailable("VideoUnavailable")