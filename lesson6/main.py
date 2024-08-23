import json
import logging
import time
import itertools

import aiofiles
import asyncio

from app.db import get_engine, make_session
from app.models import CVERecord, CveState, CnaContainer, AdpContainer
from app.utils import get_path_from_args, get_cve_filenames

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


async def read_cve_file(file_path: str):
    """Read CVE file and return its content"""
    
    try:
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            return json.loads(content)
    except Exception:
        logging.exception(f"Failed to read CVE file")


def create_objects(json_data):
    """asdasd"""
    
    result = []
    
    cve_record = CVERecord.make_from_json(json_data['cveMetadata'])
    result.append(cve_record)
    
    cna_container_data = json_data.get('containers', {}).get('cna')
    if cna_container_data:
        result.append(
            CnaContainer.make_from_json(cna_container_data, cve_record)
        )
    
    adp_containers_data = json_data.get('containers', {}).get('adp', [])
    if adp_containers_data:
        for adp_data in adp_containers_data:
            result.append(
                AdpContainer.make_from_json(adp_data, cve_record)
            )
                
    return result
    

async def process_chunk(chunk: list[str], semaphore: asyncio.Semaphore):
    """read CVE files in the given chunk"""
    
    async with semaphore:
        start_for_chunk = time.perf_counter()
    
        # read CVE files in the given chunk
        results = await asyncio.gather()
        # logging.warning("process_chunk :: before reading CVE files in the given chunk")
        tasks = [read_cve_file(file_path) for file_path in chunk]
        results = await asyncio.gather(*tasks)
        # logging.warning(f'*** reading files chunk took {(time.perf_counter() - start_for_chunk):.2f}s')
        
        cve_records = []
        cna_containers = []
        adp_containers = []
        # save CVE files into DB
        # objects = [create_objects(json_data) for json_data in results]
        for json_data in results:
            cve_record = CVERecord.make_from_json(json_data['cveMetadata'])
            cve_records.append(cve_record)
            
            cna_container_data = json_data.get('containers', {}).get('cna')
            if cna_container_data:
                cna_containers.append(
                    CnaContainer.make_from_json(cna_container_data, cve_record)
                )
            
            adp_containers_data = json_data.get('containers', {}).get('adp', [])
            if adp_containers_data:
                for adp_data in adp_containers_data:
                    adp_containers.append(
                        AdpContainer.make_from_json(adp_data, cve_record)
                    )
        
        # start_for_db = time.perf_counter()
        async with make_session(get_engine()) as session:
            # session.add_all(itertools.chain.from_iterable(objects))
            session.add_all(cve_records)
            session.add_all(cna_containers)
            session.add_all(adp_containers)
            await session.commit()
            # logging.warning(f'*** Save into db took {(time.perf_counter() - start_for_db):.2f}s')
    
        logging.warning(f'*** PROCESSSING chunk took {(time.perf_counter() - start_for_chunk):.2f}s')


async def process_cve_files(file_pathes_list: list[str]):
    """Split CVE files into chunks"""
    
    semaphore = asyncio.Semaphore(10)
    
    tasks = []
    chunksize = 5000
    start_chunk = 0
    while start_chunk <= len(file_pathes_list):
        # await process_chunk(file_pathes_list[start_chunk:start_chunk+chunksize])
        tasks.append(
            process_chunk(file_pathes_list[start_chunk:start_chunk+chunksize], semaphore)
        )
        start_chunk += chunksize
    
    await asyncio.gather(*tasks)


async def main():
    # read path to CVEs directory
    path_to_cves = get_path_from_args()
    
    # get the list of paths for CVE files
    files_list = get_cve_filenames(path_to_cves)
    logging.info(f'\nFound {len(files_list)} files.')
    # print(files_list[:5])
    print("---------")
    
    # TODO: now we should start coroutines to read our files 
    # and create CVE objects from them
    await process_cve_files(files_list)


if __name__ == "__main__":
    asyncio.run(main())