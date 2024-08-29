from datetime import datetime
from time import time
import random
import uuid

from sqlalchemy import String, Enum, Date, ForeignKey, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.constants import CveState


# cve_id_sequence = Sequence('cve_id_sequence', start=1)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class CVERecord(Base):
    __tablename__ = "cves"

    id: Mapped[str] = mapped_column(
        String(length=29),
        nullable=False,
        primary_key=True
    )
    state: Mapped[str] = mapped_column(Enum(CveState), nullable=False)
    # This UUID can be used to lookup the organization record in the user registry service.
    assigner_org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),
        comment="The UUID for the organization to which the CVE ID was originally assigned."
    )
    assigner_short_name: Mapped[str] = mapped_column(String(length=32), nullable=True)
    date_reserved: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_published: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_updated: Mapped[datetime] = mapped_column(
        Date(), nullable=True, onupdate=func.now()
    )

    cna_container: Mapped["CnaContainer"] = relationship(
        back_populates="cve_record", lazy='selectin', cascade="delete"
    )
    adp_containers: Mapped[list["AdpContainer"]] = relationship(
        back_populates="cve_record", lazy='selectin', cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<CVERecord(id={self.id})>"
    
    @staticmethod
    def generate_id():
        """Generate unique CVE id"""
        
        current_year = datetime.now().year
        random_indetifier = hex(int(time()))[2:] + str(random.randint(1, 1000))
        return f'CVE-{current_year}-fake{random_indetifier}'
    
    @classmethod
    def make_from_json(cls, data: dict):
        """asad"""
        
        if date_reserved := data.get('date_reserved'):
            date_reserved = datetime.fromisoformat(date_reserved)
        
        if date_published := data.get('date_published'):
            date_published = datetime.fromisoformat(date_published)
        
        if date_updated := data.get('date_updated'):
            date_updated = datetime.fromisoformat(date_updated)
        
        return cls(
            id=data['id'],
            state=data['state'],
            assigner_org_id=data['assigner_org_id'],
            assigner_short_name=data.get('assigner_short_name'),
            date_reserved=date_reserved,
            date_published=date_published,
            date_updated=date_updated,
        )


class CnaContainer(Base):
    __tablename__ = "cna_containers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=256), nullable=True)
    description: Mapped[str] = mapped_column(String(length=4096), nullable=False)
    date_assigned: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_public: Mapped[datetime] = mapped_column(Date(), nullable=True)

    cve_record_id: Mapped[str] = mapped_column(ForeignKey("cves.id", ondelete="CASCADE"), nullable=False)
    cve_record: Mapped["CVERecord"] = relationship(back_populates="cna_container", lazy='selectin')
    
    def __repr__(self) -> str:
        _title = f'{self.title[:30]}...' if self.title else None
        # return f"<CnaContainer(id={self.id}, title={self.title[:30]}...)>"
        return f"<CnaContainer(id={self.id}, title={_title})>"

    @classmethod
    def make_from_json(cls, data: dict, cve_id: str):        
        if date_assigned := data.get('date_assigned'):
            date_assigned = datetime.fromisoformat(date_assigned)
        
        if date_public := data.get('date_public'):
            date_public = datetime.fromisoformat(date_public)
        
        return cls(
            title=data.get('title'),
            description=data.get('description'),
            date_assigned=date_assigned,
            date_public=date_public,
            cve_record_id=cve_id
        )


class AdpContainer(Base):
    __tablename__ = "adp_containers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=256), nullable=True)
    description: Mapped[str] = mapped_column(String(length=4096), nullable=True)
    date_assigned: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_public: Mapped[datetime] = mapped_column(Date(), nullable=True)
    
    cve_record_id: Mapped[str] = mapped_column(ForeignKey("cves.id", ondelete="CASCADE"), nullable=False)
    cve_record: Mapped["CVERecord"] = relationship(back_populates="adp_containers", lazy='selectin')

    def __repr__(self) -> str:
        _title = f'{self.title[:30]}...' if self.title else None
        # return f"<AdpContainer(id={self.id}, title={self.title[:30]}...)>"
        return f"<AdpContainer(id={self.id}, title={_title})>"

    @classmethod
    def make_from_json(cls, data: dict, cve_id: str):
        if date_assigned := data.get('date_assigned'):
            date_assigned = datetime.fromisoformat(date_assigned)
        
        if date_public := data.get('date_public'):
            date_public = datetime.fromisoformat(date_public)
        
        return cls(
            title=data.get('title'),
            description=data.get('description'),
            date_assigned=date_assigned,
            date_public=date_public,
            cve_record_id=cve_id
        )
