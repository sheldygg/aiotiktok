import json
import re
from http import HTTPMethod
from typing import Any, Callable, cast
from urllib.parse import urljoin

from aiohttp import ClientSession

from .exceptions import UrlUnavailable, VideoUnavailable
from .types import Aweme


class TikTokClient:
    def __init__(
        self,
        host: str | None = None,
        json_loads: Callable[..., dict[str, Any]] = json.loads,
    ):
        self.host = (
            "https://api22-normal-c-alisg.tiktokv.com/" if host is None else host
        )
        self.json_loads = json_loads

        self._session = ClientSession()

    async def close(self) -> None:
        await self._session.close()

    async def _make_request(
        self, method: HTTPMethod, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        async with self._session.request(
            method, urljoin(self.host, endpoint), **kwargs
        ) as response:
            return cast(dict[str, Any], await response.json(loads=self.json_loads))

    async def get_video_id(self, video_url: str) -> str:
        async with self._session.get(video_url) as response:
            web_url = str(response.url)

        if (
            web_url == "https://tiktok.com"
            or "video" not in web_url
            and "photo" not in web_url
        ):
            raise UrlUnavailable(video_url)
        video_id_match = re.findall("/(?:photo|video)/(\d+)", web_url)
        if not video_id_match:
            raise UrlUnavailable(video_url)
        return cast(str, video_id_match[0])

    async def get_video_data(
        self, video_url: str | None = None, video_id: str | None = None
    ) -> Aweme:
        if not video_url and not video_id:
            raise ValueError("You must provide either a video_url or video_id")

        if not video_id and video_url:
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
            "aweme_id": video_id,
        }
        data = await self._make_request(HTTPMethod.OPTIONS, "aweme/v1/feed/", params=params)

        for aweme in data["aweme_list"]:
            if aweme["aweme_id"] == video_id:
                return Aweme.from_dict(aweme)

        raise VideoUnavailable(video_id)
