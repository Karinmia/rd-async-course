import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import cves


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def initialize_app() -> FastAPI:
    _app = FastAPI(title="CVE CRUD API")
    
    _app.include_router(cves.router)
    
    add_pagination(_app)
    
    return _app
    
    
app = initialize_app()


@app.get("/", tags=['general'])
@app.get("/healthcheck", tags=['general'])
def health_check():
    return {"status": "alive"}
