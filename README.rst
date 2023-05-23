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

Simple Request
========

.. code-block:: python

   import asyncio
   from aiotiktok import Client

   tiktok = Client()


   async def main():
       await tiktok.get_data(url="some url")


   asyncio.run(main())

Signature
=======

**For use method user_feed_sig you must up your application.**

This must be done in order to be able to generate a signature for a request to the private TikTok api

Follow this instruction https://github.com/sheldygg/tiktok-signature

After you have run it, you must specify a reference when initializing the Client class

.. code-block:: python

    from aiotiktok import Client

    tiktok = Client(signature_url="some url")

By default is http://127.0.0.1:8002/signature

Then you can get user feed

.. code-block:: python

    from aiotiktok import Client

    tiktok = Client()

    await tiktok.user_feed_sig("playboicarti")