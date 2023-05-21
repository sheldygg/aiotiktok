import json
import re
from urllib.parse import urlencode, urljoin

from httpx import AsyncClient

from .constants import (default_user_videos_params,
                        static_unsigned_user_videos, static_user_videos_url)
from .exceptions import URLUnavailable, VideoUnavailable
from .extractors import (extract_data_from_html, extract_user_data,
                         extract_video_data)
from .types import Author, VideoData


class Client:
    def __init__(self, signature_url: str = "http://127.0.0.1:8002/signature") -> None:
        self.signature_url = signature_url
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
        method: str = "GET",
        params: dict | None = None,
        data: dict | str | None = None,
        headers: dict | None = None,
        allow_redirects: bool = True,
    ):
        async with AsyncClient() as session:
            response = await session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                follow_redirects=allow_redirects,
            )
            response_headers = response.headers
            try:
                response = response.json()
            except json.decoder.JSONDecodeError:
                response = response.read()
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
        self, url: str | None = None, video_id: str | int | None = None
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
        if data and data.get("aweme_id") == str(video_id):
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
        data = extract_data_from_html(response.get("response").decode())
        item_module = data.get("ItemModule")
        videos = []
        for video in list(item_module.values())[:count]:
            videos.append(await self.get_data(video_id=video.get("id")))
        return videos

    async def user_info(self, username: str) -> Author:
        """
        Get UserInfo
        :param username:
        :return:
        """
        url = urljoin(self.base_url, f"@{username}")
        response = await self._request(url, headers=self.headers)
        data = extract_data_from_html(response.get("response").decode())
        return extract_user_data(data)

    async def sign_url(self, url: str):
        request = await self._request(
            url=self.signature_url, method="POST", data={"url": url}
        )
        return request.get("response", {})

    async def _get_user_feed_private(self, username: str, count: int | None = None):
        sec_uid = (await self.user_info(username)).sec_uid
        params = default_user_videos_params
        params.update({"secUid": sec_uid})
        unsigned_url = f"{static_unsigned_user_videos}{urlencode(params)}"
        signature_data = await self.sign_url(unsigned_url)
        headers = {
            "x-tt-params": signature_data.get("x-tt-params"),
            "user-agent": signature_data.get("navigator", {}).get("user_agent"),
        }
        api_response = (
            await self._request(url=static_user_videos_url, headers=headers)
        ).get("response")
        user_videos = [video for video in api_response.get("itemList", [])]
        has_more = api_response.get("hasMore")
        while has_more and len(user_videos) < count if count else None:
            cursor = api_response.get("cursor")
            params.update({"cursor": cursor})
            unsigned_url = f"{static_unsigned_user_videos}{urlencode(params)}"
            signature_data = await self.sign_url(unsigned_url)
            headers.update({"x-tt-params": signature_data.get("x-tt-params")})
            api_response = (
                await self._request(url=static_user_videos_url, headers=headers)
            ).get("response")
            user_videos.extend(api_response.get("itemList"))
            has_more = api_response.get("hasMore")
        return user_videos

    async def user_feed_sig(self, username: str, count: int | None = None):
        """
        Get user feed with private signature, for use that method you must up your application
        https://github.com/sheldygg/aiotiktok#signature
        :param username:
        :param count:
        :return:
        """
        videos = []
        user_videos = (await self._get_user_feed_private(username))[:count]
        for video in user_videos:
            videos.append(await self.get_data(video_id=video.get("id")))
        return videos
