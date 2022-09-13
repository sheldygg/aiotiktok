# AIOtiktok

[![PyPi Package Version](https://img.shields.io/pypi/v/aiotiktok)](https://pypi.org/project/aiotiktok/)

**aiotiktok** super simple and fast library to get all video data from tiktok


**One step before start.**
- You must install library with pip `pip install aiotiktok`
- or `pip install git+https://github.com/sheldygg/aiotiktok`

### Request

```python
import asyncio
from aiotiktok import Tiktok

tiktok = Tiktok()

async def main():
    data = await tiktok.tiktok(original_url="some url")
    print(data)
    
asyncio.run(main())
```
