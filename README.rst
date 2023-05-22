# aiotiktok

[![PyPi Package Version](https://img.shields.io/pypi/v/aiotiktok?color=blue)](https://pypi.org/project/aiotiktok/)
[![Downloads](https://img.shields.io/pypi/dm/aiotiktok?color=blue)](https://pypi.org/project/aiotiktok/)

**aiotiktok** super simple and fast library to get all video data from TikTok


**One step before start.**
- You must install a library with pip `pip install aiotiktok`

### Request

```python
import asyncio
from aiotiktok import Client

tiktok = Client()


async def main():
    data = await tiktok.video_data(url="some url")
    print(data)


asyncio.run(main())
```

### Signature

**For use method user_feed_sig you must up your application.**

This must be done in order to be able to generate a signature for a request to the private TikTok api

Follow this instruction https://github.com/sheldygg/tiktok-signature

After you have run it, you must specify a reference when initializing the Client class
```python
from aiotiktok import Client

tiktok = Client(signature_url="your url")
```
By default is http://127.0.0.1:8002/signature

Then you can get user feed
```python
from aiotiktok import Client

tiktok = Client()

await tiktok.user_feed_sig("playboicarti")
```