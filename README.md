# aiotiktok

[![PyPi Package Version](https://img.shields.io/pypi/v/aiotiktok?color=blue)](https://pypi.python.org/pypi/aiotiktok)
[![Downloads](https://img.shields.io/pypi/dm/aiotiktok?color=blue)](https://pypi.python.org/pypi/aiotiktok)

**aiotiktok** is a super simple and fast library for retrieving all video data from TikTok.

## Simple Request

```python
import asyncio

from aiotiktok.client import TikTokClient


async def main():
    client = TikTokClient()

    await client.get_video_data(video_id="7349190849017744646")
    
    await client.close()


asyncio.run(main())

```

