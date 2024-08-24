import logging

import aiohttp
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


logging.basicConfig(level=logging.DEBUG)

async def homepage(request):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/delay/2") as response:
            await response.text()
            
    return PlainTextResponse("Hello, world!")


app = Starlette(
    routes=[
        Route("/", homepage),
    ],
)
