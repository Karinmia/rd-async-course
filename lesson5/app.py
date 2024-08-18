import os
import time

from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

import asyncio

from functions import mp_count_words

FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "ära"


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    print(f"{msg} took {time.perf_counter() - start:.2f} seconds")


def reduce_words(target: dict, source: dict) -> dict:
    for key, value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value
    return target


async def monitoring(counter, counter_lock, total):
    interval_seconds = 0.5  # can be adjusted

    while True:
        # with counter_lock:
        print(f"Progress: {counter.value}/{total}")
        if counter.value == total:
            break
        await asyncio.sleep(interval_seconds)


def get_file_chunks(
    cpu_count: int,
    file_size: int,
) -> list[tuple[int, int]]:
    """Split file into chunks"""

    chunk_size = file_size // cpu_count
    print(f"{chunk_size = }")
    
    start_end = list()
    # with open(FILE_PATH, encoding="utf-8", mode="r+b") as f:
    with open(FILE_PATH, mode="r+b") as f:

        def is_new_line(position):
            if position == 0:
                return True
            else:
                f.seek(position - 1)
                return f.read(1) == b"\n"

        def next_line(position):
            f.seek(position)
            f.readline()
            return f.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_new_line(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)

            start_end.append(
                (
                    chunk_start,
                    chunk_end,
                )
            )

            chunk_start = chunk_end

    return start_end


async def main():
    loop = asyncio.get_event_loop()
    
    cpu_count = mp.cpu_count()
    file_size = os.path.getsize(FILE_PATH)
    
    with timer("Get file chunks"):
        file_chunks = get_file_chunks(cpu_count, file_size)

    with mp.Manager() as manager:
        counter = manager.Value("i", 0)
        counter_lock = manager.Lock()

        monitoring_task = asyncio.shield(
            asyncio.create_task(monitoring(counter, counter_lock, file_size))
        )

        with ProcessPoolExecutor(max_workers=cpu_count) as executor:
            with timer("Processing data"):
                results = []
                for chunk_start, chunk_end in file_chunks:
                    results.append(
                        loop.run_in_executor(
                            executor,
                            mp_count_words,
                            FILE_PATH,
                            chunk_start,
                            chunk_end,
                            counter,
                            counter_lock,
                        )
                    )

                done, _ = await asyncio.wait(results)

        monitoring_task.cancel()

    # Combine all results from all chunks
    words = {}
    with timer("\nReducing results"):
        for result in done:
            words = reduce_words(words, result.result())

    with timer("\nPrinting results"):
        print(f"\nTotal words: {len(words)}")
        print(f"Total count for word: {words[WORD]}")


if __name__ == "__main__":
    with timer("Total time"):
        asyncio.run(main())
