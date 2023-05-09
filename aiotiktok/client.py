import re
from urllib.parse import urljoin

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError

from .exceptions import URLUnavailable, VideoUnavailable
from .extractors import extract_user_feed, extract_video_data
from .types import VideoData


class Client:
    def __init__(
        self, client_id: str | None = None, client_secret: str | None = None
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_headers = {
            "user-agent": "com.ss.android.ugc.trill/2613 (Linux; U; Android 10; en_US; Pixel 4; "
            "Build/QQ3A.200805.001; Cronet/58.0.2991.0)"
        }
        self.base_url = "https://www.tiktok.com/"
        self.api_url = (
            "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={}"
        )
        self.headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }

    async def _request(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
        allow_redirects: bool = False,
    ):
        async with ClientSession() as session:
            async with session.get(
                url=url,
                params=params,
                data=data,
                headers=headers,
                allow_redirects=allow_redirects,
            ) as resp:
                response_headers = resp.headers
                try:
                    response = await resp.json()
                except ContentTypeError:
                    response = await resp.read()
        return dict(response=response, headers=response_headers)

    async def get_video_id(self, url: str):
        if "@" in url:
            pass
        else:
            headers = (await self._request(url, allow_redirects=False)).get("headers")
            url = headers.get("Location").split("?")[0]
        if url == self.base_url or "video" not in url:
            raise URLUnavailable("URLUnavailable, check the link")
        video_id = re.findall("/video/(\d+)?", url)[0]
        return video_id

    async def get_data(
        self, url: str | None = None, video_id: str | None = None
    ) -> VideoData:
        """
        Get TikTok data
        :param video_id: id of video:
        :param url: url to video
        :return: :class:`aiotiktok.types.VideoData`
        """
        if video_id is None:
            video_id = await self.get_video_id(url)
        api_link = self.api_url.format(video_id)
        data = (
            (await self._request(api_link, headers=self.api_headers))
            .get("response", {})
            .get("aweme_list", {})[0]
        )
        if data and data.get("aweme_id") == video_id:
            return extract_video_data(data)
        raise VideoUnavailable("VideoUnavailable")

    async def user_feed(self, username: str, count: int = None) -> list[VideoData]:
        """
        Get User Feed
        :param username:
        :param count:
        :return: list[:class:`aiotiktok.types.VideoData`]
        """
        url = urljoin(self.base_url, f"@{username}")
        response = await self._request(url, headers=self.headers)
        data = extract_user_feed(response.get("response").decode())
        item_module = data.get("ItemModule")
        videos = []
        for video in list(item_module.values())[:count]:
            videos.append(await self.get_data(video_id=video.get("id")))
        return videos
