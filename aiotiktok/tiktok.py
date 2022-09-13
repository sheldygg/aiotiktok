import re

from aiohttp import ClientSession


class Tiktok():
    def __init__(self) -> None:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }
        self.tiktok_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "authority": "www.tiktok.com",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Host": "www.tiktok.com",
            "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
        }
        self.tiktok_api_link = "https://api.tiktokv.com/aweme/v1/aweme/detail/?aweme_id={}"

    async def make_session(self):
        self.session = ClientSession()
    
    async def close_session(self):
        await self.session.close()

    async def get_video_id(self, original_url: str):
        if "@" in original_url:
            return original_url
        else:
            await self.make_session()
            resp = await self.session.get(url=original_url, allow_redirects=False)
            original_url = resp.headers["Location"].split("?")[0]
            await self.close_session()
        return original_url

    async def tiktok(self, original_url: str):
        original_url = await self.get_video_id(original_url)
        video_id = re.findall('/video/(\d+)?', original_url)[0]
        
        await self.make_session()
        response = await self.session.get(self.tiktok_api_link.format(video_id), headers=self.headers)
        predata = await response.json()
        await self.close_session()
        try:
            data = predata["aweme_detail"]
            if "image_post_info" in data:
                video_type = "album"
                media = []
                for images in data["image_post_info"]["images"]:
                    media.append(images["display_image"]["url_list"][0])
            else:
                video_type = "video"
                media = data["video"]["play_addr"]["url_list"][0]
            cover = data['video']['cover']['url_list'][0]
            dynamic_cover = data['video']['dynamic_cover']['url_list'][0]
            desc = data["desc"]
            comment_count = data["statistics"]["comment_count"]
            play_count = data["statistics"]["play_count"]
            download_count = data["statistics"]["download_count"]
            share_count = data["statistics"]["share_count"]
            create_time = data["create_time"]
            author_name = data["author"]["nickname"]
            author_nick = data["author"]["unique_id"]
            author_pic = data["author"]["avatar_larger"]["url_list"][0]
            music_title = data['music']['title']
            music_author = data['music']['author']
            music_url = data['music']['play_url']['url_list'][0]
            music_cover = data["music"]["cover_large"]["url_list"][0]
            video_info = {"status": "succes",
                        "video_type": video_type,
                        "media": media,
                        "cover": cover,
                        "dynamic_cover": dynamic_cover,
                        "desc": desc,
                        "play_count": play_count,
                        "comment_count": comment_count,
                        "download_count": download_count,
                        "share_count": share_count,
                        "create_time": create_time,
                        "author_name": author_name,
                        "author_nick": author_nick,
                        "author_pic": author_pic,
                        "music_title": music_title,
                        "music_author": music_author,
                        "music_url": music_url,
                        "music_cover": music_cover
            }
        except Exception as e:
            video_info = {"status": "failed", "except": e}
        return video_info