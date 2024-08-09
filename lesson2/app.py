"""
Homework for the second lesson.
"""

import argparse
import logging
import time

import asyncio
import aiohttp
import aiofiles

logging.basicConfig(level=logging.INFO)


async def aenumerate(asequence, start=0):
    """Asynchronously enumerate an async iterator from a given start value"""
    n = start
    async for elem in asequence:
        yield n, elem
        n += 1


def get_filename_from_args() -> str:
    parser = argparse.ArgumentParser(
        prog='lesson2',
        description='Read file with urls and write their content to separate files.'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    return args.filename


async def write_content_to_file(idx: int, content: str):
    output_filename = f'{idx}_output.txt'
    try:
        async with aiofiles.open(output_filename, 'w') as f:
            await f.write(content)
    except Exception as e:
        logging.error("Failed to write_content_to_file")


async def process_url(session: aiohttp.ClientSession, url: str, idx: int):
    """Get content from the given URL and write it to the file"""
    
    try:
        async with asyncio.timeout(3):
            async with session.get(url, ssl=False) as response:
                content = await response.text()
    except asyncio.TimeoutError:
        logging.error(f"The long operation timed out, {idx = }, {url = }")
    except Exception as e:
        logging.error(f"Failed to get response, {idx = }, {url = }")
    else:
        await write_content_to_file(idx, content)


async def main():
    # read filename from script arguments
    filename = get_filename_from_args()
    logging.info(f'Start reading from {filename}')
    
    try:
        async with aiofiles.open(filename) as f:
            async with aiohttp.ClientSession() as session:
                await asyncio.gather(*[
                    process_url(session, line, idx)
                    async for idx, line in aenumerate(f)
                ])
    except OSError:
        logging.error("Failed to read from the given file. Please check if it exists and try again.")
    except Exception as e:
        logging.error(f"Something went wrong, error = {e}")


start_time = time.time()
asyncio.run(main())
total_time = time.time() - start_time
logging.info("***************")
logging.info(f"Completed in {total_time:.2f}s")
