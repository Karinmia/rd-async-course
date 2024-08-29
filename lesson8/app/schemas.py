import enum
import uuid
from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, StringConstraints, Field

from app.constants import CveState


class CVERecordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    state: CveState
    assigner_org_id: uuid.UUID
    assigner_short_name: Annotated[str, StringConstraints(strip_whitespace=True, max_length=32)]
    description: str | None = None
    date_reserved: datetime | None = None
    date_published: datetime | None = None
    date_updated: datetime | None = None


class CnaContainerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: Annotated[str, StringConstraints(strip_whitespace=True, max_length=256)] | None = None
    description: Annotated[str, StringConstraints(strip_whitespace=True, max_length=4096)] | None = None
    date_assigned: datetime | None = None
    date_public: datetime | None = None


class AdpContainerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: Annotated[str, StringConstraints(strip_whitespace=True, max_length=256)] | None = None
    description: Annotated[str, StringConstraints(strip_whitespace=True, max_length=4096)] | None = None
    date_assigned: datetime | None = None
    date_public: datetime | None = None


class GetCVERecordSchema(BaseModel):
    id: str
    state: CveState
    assigner_org_id: uuid.UUID
    assigner_short_name: str | None = None
    description: str | None = None
    date_reserved: datetime | None = None
    date_published: datetime | None = None
    date_updated: datetime | None = None
    cna_container: CnaContainerSchema | None = None
    adp_containers: list[AdpContainerSchema] = list()
    

class CreateCnaContainerSchema(BaseModel):
    title: Annotated[str, StringConstraints(max_length=256)] | None = None
    description: Annotated[str, StringConstraints(max_length=4096)] | None = None
    date_assigned: datetime | None = None
    date_public: datetime | None = None


class CreateAdpContainerSchema(BaseModel):
    title: Annotated[str, StringConstraints(max_length=256)] | None = None
    description: Annotated[str, StringConstraints(max_length=4096)] | None = None
    date_assigned: datetime | None = None
    date_public: datetime | None = None


class CreateCVERecordSchema(BaseModel):
    state: CveState = CveState.PUBLISHED
    assigner_org_id: uuid.UUID
    assigner_short_name: Annotated[str, StringConstraints(strip_whitespace=True, max_length=32)] | None = None
    date_reserved: datetime | None = None
    date_published: datetime | None = None
    date_updated: datetime | None = None
    cna_container: CreateCnaContainerSchema | None = None
    adp_containers: list[CreateAdpContainerSchema] = Field(description='same structure as cna_container', default=[])
    

class BaseResponseSchema(BaseModel):
	success: bool


class ResponseOnCreate(BaseResponseSchema):
    cve_id: str
