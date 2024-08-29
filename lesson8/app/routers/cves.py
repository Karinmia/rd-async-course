import json
from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, JSONResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from app.models import CVERecord, CnaContainer, AdpContainer
from app.schemas import (
    CVERecordSchema, GetCVERecordSchema, CreateCVERecordSchema, ResponseOnCreate
)


router = APIRouter(
    prefix="/cves",
    tags=["cves"],
    responses={404: {"description": "Not found"}},
)

# define session dependency to reuse it in the relevant APIs
SessionDep = Depends(get_session)


@router.get("/")
async def list_cve_records(session: AsyncSession = SessionDep) -> Page[CVERecordSchema]:
    """Returns basic info about CVE records (without containers info)"""
    
    # TODO: implement filtering
    # query = select(CVERecord)
    # query = user_filter.filter(query)
    # query = user_filter.sort(query)
    # result = await db.execute(query)
    # return result.scalars().all()
    
    return await paginate(session, select(CVERecord))


@router.post("/")
async def create_cve_record(
    data: CreateCVERecordSchema,
    session: AsyncSession = SessionDep
) -> ResponseOnCreate:
    """Create CVE record alongside its containers (cna, adp)"""
    
    entities_to_create = []
    
    cve_record_data = data.model_dump()
    cve_record_id = CVERecord.generate_id()
    
    cna_container_data = cve_record_data.pop('cna_container')
    adp_containers_data = cve_record_data.pop('adp_containers')
    
    cve_record_data['id'] = cve_record_id
    entities_to_create.append(CVERecord(**cve_record_data))
    
    if cna_container_data:
        cna_container_data['cve_record_id'] = cve_record_id
        entities_to_create.append(CnaContainer(**cna_container_data))
    
    for adp_cont in adp_containers_data:
        adp_cont['cve_record_id'] = cve_record_id
        entities_to_create.append(AdpContainer(**adp_cont))
    
    session.add_all(entities_to_create)
    await session.commit()
    
    return {"success": True, 'cve_id': cve_record_id}


@router.get("/{cve_id}")
async def get_cve_record(cve_id: str, session: AsyncSession = SessionDep) -> GetCVERecordSchema:
    """Returns full info about CVE records (with containers info)"""
    cve_record = await session.get(CVERecord, cve_id)
    if cve_record:
        return cve_record
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{cve_id}")
async def update_cve_record(cve_id: str, session: AsyncSession = SessionDep) -> JSONResponse:
    """
    ***NOT IMPLEMENTED***
    Update CVE record.
    """
    return JSONResponse(
        content={"message": "Not implemented"},
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )


@router.delete("/{cve_id}")
async def delete_cve_record(cve_id: str, session: AsyncSession = SessionDep) -> Response:
    """Delete CVE record and all connected data by CVE id"""
    
    cve_record = await session.get(CVERecord, cve_id)
    if cve_record:
        await session.delete(cve_record)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
