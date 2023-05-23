####################
aiotiktok
####################

.. image:: https://img.shields.io/pypi/v/aiotiktok?color=blue
    :target: https://pypi.python.org/pypi/aiotiktok
    :alt: PyPi Package Version

.. image:: https://img.shields.io/pypi/dm/aiotiktok?color=blue
    :target: https://pypi.python.org/pypi/aiotiktok
    :alt: Downloads

**aiotiktok** is super simple and fast library
to get all video data from TikTok

**Request**

.. code-block:: python
    :linenos:

    import asyncio
    from aiotiktok import Client

    tiktok = Client()


    async def main():
        data = await tiktok.video_data(url="some url")
        print(data)


    asyncio.run(main())
