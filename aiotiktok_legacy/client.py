import json
import re
from urllib.parse import urlencode, urljoin

from httpx import AsyncClient

from .constants import (
    default_user_videos_params,
    static_unsigned_user_videos,
    static_user_videos_url,
)
from .exceptions import URLUnavailable, VideoUnavailable
from .extractors import extract_data_from_html, extract_user_data, extract_video_data
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
            "https://api22-normal-c-alisg.tiktokv.com/aweme/v1/feed/"
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
        data: dict | None = None,
        headers: dict | None = None,
        allow_redirects: bool = True,
    ) -> dict:
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
                response_data = response.json()
            except json.decoder.JSONDecodeError:
                response_data = response.read()
        return dict(response=response_data, headers=response_headers)

    async def get_video_id(self, url: str) -> str:
        if "@" not in url:
            headers = (await self._request(url, allow_redirects=False)).get(
                "headers", {}
            )
            url = headers.get("Location").split("?")[0]
        if url == self.base_url or "video" not in url and "photo" not in url:
            raise URLUnavailable("URLUnavailable, check the link")
        video_id_match = re.findall("/(?:photo|video)/(\d+)", url)
        if not video_id_match:
            raise URLUnavailable("URLUnavailable, check the link")
        return video_id_match[0]

    async def video_data(
        self, url: str | None = None, video_id: str | int | None = None
    ) -> VideoData:
        """
        Get TikTok data
        :param video_id: id of video:
        :param url: url to video
        :return: :class:`aiotiktok.types.VideoData`
        """
        if video_id is None and url:
            video_id = await self.get_video_id(url)
        api_link = self.api_url.format(video_id)

        params = {
            # "passport-sdk-version": "19",
            "iid": "7318518857994389254",
            "device_id": "7318517321748022790",

            # "ac": "wifi",
            "channel": "googleplay",
            # "aid": "1233",

            "app_name": "musical_ly",
            "version_code": "300904",
            # "version_name": "30.9.4",
            "device_platform": "android",
            # "os": "android",
            # "ab_version": "30.9.4",
            # "ssmix": "a",
            "device_type": "ASUS_Z01QD",
            # "device_brand": "Asus",

            # "language": "en",
            # "os_api": "28",
            "os_version": "9",

            # "openudid": "704713c0da01388a",
            # "manifest_version_code": "2023009040",
            # "resolution": "1600*900",
            # "dpi": "300",
            # "update_version_code": "2023009040",
            # "_rticket": "1692845349183",
            # "is_pad": "0",
            # "current_region": "BE",
            # "app_type": "normal",
            # "sys_region": "US",
            # "mcc_mnc": "20610",
            # "timezone_name": "Asia/Shanghai",
            # "residence": "BE",
            # "app_language": "en",
            # "carrier_region": "BE",
            # "ac2": "wifi",
            # "uoo": "0",
            # "op_region": "BE",
            # "timezone_offset": "28800",
            # "build_number": "30.9.4",
            # "host_abi": "arm64-v8a",
            # "locale": "en",
            # "region": "US",
            # "ts": "1692845349",
            # "cdid": "60c2140f-c112-491a-8c93-183fd1ea8acf",
            # "support_webview": "1",
            # "okhttp_version": "4.1.120.34-tiktok",
            # "use_store_region_cookie": "1",
            "aweme_id": video_id
        }

        data = (
            (await self._request(self.api_url, params=params, headers={"x-lagon": '1'}))
            .get("response", {})
            .get("aweme_list", {})[0]
        )
        if data and data.get("aweme_id") == str(video_id):
            return extract_video_data(data)
        raise VideoUnavailable("VideoUnavailable")

    async def user_feed(
        self, username: str, count: int | None = None
    ) -> list[VideoData]:
        """
        Get user feed, only 30 videos.
        :param username:
        :param count:
        :return: list[:class:`aiotiktok.types.VideoData`]
        """
        url = urljoin(self.base_url, f"@{username}")
        response = await self._request(url, headers=self.headers)
        data = extract_data_from_html(response.get("response", b"").decode())
        item_module = data.get("ItemModule")
        videos = []
        for video in list(item_module.values())[:count]:
            videos.append(await self.video_data(video_id=video.get("id")))
        return videos

    async def user_info(self, username: str) -> Author:
        """
        Get UserInfo
        :param username:
        :return :class:`aiotiktok.types.Author`:
        """
        url = urljoin(self.base_url, f"@{username}")
        response = await self._request(url, headers=self.headers)
        data = extract_data_from_html(response.get("response", b"").decode())
        return extract_user_data(data)

    async def sign_url(self, url: str) -> dict:
        request = await self._request(
            url=self.signature_url, method="POST", data={"url": url}
        )
        return request.get("response", {})

    async def _get_user_feed_private(
        self, username: str, count: int | None = None
    ) -> list[dict]:
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
        ).get("response", {})
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

    async def user_feed_sig(
        self, username: str, count: int | None = None
    ) -> list[VideoData]:
        """
        Get user feed with private signature, for use that method you must up your application
        https://github.com/sheldygg/aiotiktok#signature
        :param username:
        :param count:
        :return: list[:class:`aiotiktok.types.VideoData`]
        """
        videos = []
        user_videos = (await self._get_user_feed_private(username))[:count]
        for video in user_videos:
            videos.append(await self.video_data(video_id=video.get("id")))
        return videos
