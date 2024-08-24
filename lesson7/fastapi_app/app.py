import aiohttp
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/delay/2") as response:
            await response.text()
    return {"message": "Hello, world!"}
