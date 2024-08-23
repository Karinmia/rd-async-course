import os
import logging

import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.config import DB_URI
from app.utils import get_path_from_args, get_cve_filenames

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DB_ECHO = os.environ.get("DB_ECHO", "false").lower() == "true"


def get_engine() -> AsyncEngine:
    return create_async_engine(DB_URI, echo=DB_ECHO)


def make_session_class(engine: AsyncEngine) -> type[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def main():
    # read path to CVEs directory
    path_to_cves = get_path_from_args()
    
    # get the list of paths for CVE files
    files_list = get_cve_filenames(path_to_cves)
    print(f'\nFound {len(files_list)} files.')
    print(files_list[:5])
    
    # TODO: now we should start coroutines to read our files 
    # and create CVE objects from them


if __name__ == "__main__":
    asyncio.run(main())