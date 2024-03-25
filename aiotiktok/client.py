import re

from aiohttp import ClientSession

from urllib.parse import urljoin
from http import HTTPMethod

from .types import Aweme
from .exceptions import UrlUnavailable


class TikTokClient:
    def __init__(self, host: str | None = None):
        self.host = "https://api22-normal-c-alisg.tiktokv.com/" if host is None else host

        self._session = ClientSession()

    async def close(self):
        await self._session.close()

    async def _make_request(self, method: HTTPMethod, endpoint: str, **kwargs) -> dict:
        async with self._session.request(
            method,
            urljoin(self.host, endpoint),
            **kwargs
        ) as response:
            return await response.json()

    async def get_video_id(self, video_url: str) -> str:
        async with self._session.get(video_url) as response:
            web_url = str(response.url)

        if web_url == "https://tiktok.com" or "video" not in web_url and "photo" not in web_url:
            raise UrlUnavailable(video_url)
        video_id_match = re.findall("/(?:photo|video)/(\d+)", web_url)
        if not video_id_match:
            raise UrlUnavailable(video_url)
        return video_id_match[0]

    async def get_video_data(self, video_url: str | None = None, video_id: str | None = None) -> Aweme:
        if not video_url and not video_id:
            raise ValueError("You must provide either a video_url or video_id")

        if not video_id:
            video_id = await self.get_video_id(video_url)

        params = {
            "iid": "7318518857994389254",
            "device_id": "7318517321748022790",
            "channel": "googleplay",
            "app_name": "musical_ly",
            "version_code": "300904",
            "device_platform": "android",
            "device_type": "ASUS_Z01QD",
            "os_version": "9",
            "aweme_id": video_id
        }
        data = (await self._make_request(HTTPMethod.GET, "aweme/v1/feed/", params=params))
        aweme_raw_data = data["aweme_list"][0]

        return Aweme.from_dict(aweme_raw_data)
