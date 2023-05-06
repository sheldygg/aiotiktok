# AIOtiktok

[![PyPi Package Version](https://img.shields.io/pypi/v/aiotiktok?color=blue)](https://pypi.org/project/aiotiktok/)
[![Downloads](https://img.shields.io/pypi/dm/aiotiktok?color=blue)](https://pypi.org/project/aiotiktok/)

**aiotiktok** super simple and fast library to get all video data from TikTok


**One step before start.**
- You must install library with pip `pip install aiotiktok`
- or `pip install git+https://github.com/sheldygg/aiotiktok`

### Request

```python
import asyncio
from aiotiktok import Client

tiktok = Client()

async def main():
    data = await tiktok.get_data(url="some url")
    print(data)
    
asyncio.run(main())
```
