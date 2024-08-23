from datetime import datetime
import enum
import uuid

from sqlalchemy import CheckConstraint, String, Enum, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class CveState(enum.Enum):
    PUBLISHED = "PUBLISHED"
    RESERVED = "RESERVED"
    REJECTED = "REJECTED"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class CVERecord(Base):
    __tablename__ = "cves"
    # Regular expression for validation
    # __table_args__ = (
    #     CheckConstraint("id ~ '^CVE-[0-9]{4}-[0-9]{4,19}$'", name='valid_cve_id'),
    # )

    id: Mapped[str] = mapped_column(
        String(length=29),
        nullable=False,
        primary_key=True
    )
    state: Mapped[str] = mapped_column(Enum(CveState), nullable=False)
    # This UUID can be used to lookup the organization record in the user registry service.
    assigner_org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        # primary_key=True,
        # unique=True,
        server_default=func.gen_random_uuid(),
        comment="The UUID for the organization to which the CVE ID was originally assigned."
    )
    assigner_short_name: Mapped[str] = mapped_column(String(length=32), nullable=True)
    date_reserved: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_published: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_updated: Mapped[datetime] = mapped_column(
        Date(),
        nullable=True,
        onupdate=func.now()
    )

    cna_container: Mapped["CnaContainer"] = relationship(back_populates="cve_record")
    adp_containers: Mapped[list["AdpContainer"]] = relationship(back_populates="cve_record")

    def __repr__(self) -> str:
        return f"<CVERecord(id={self.id})>"
    
    @classmethod
    def make_from_json(cls, data: dict):
        """asad"""
        
        if date_reserved := data.get('dateReserved'):
            date_reserved = datetime.fromisoformat(date_reserved)
        
        if date_published := data.get('datePublished'):
            date_published = datetime.fromisoformat(date_published)
        
        if date_updated := data.get('dateUpdated'):
            date_updated = datetime.fromisoformat(date_updated)
        
        return cls(
            id=data['cveId'],
            state=data['state'],
            assigner_org_id=data['assignerOrgId'],
            assigner_short_name=data.get('assignerShortName'),
            date_reserved=date_reserved,
            date_published=date_published,
            date_updated=date_updated,
        )


class CnaContainer(Base):
    __tablename__ = "cna_containers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=256), nullable=True)
    description: Mapped[str] = mapped_column(
        String(length=4096),
        nullable=False,
    )
    date_assigned: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_public: Mapped[datetime] = mapped_column(Date(), nullable=True)

    cve_record_id: Mapped[str] = mapped_column(ForeignKey("cves.id"), nullable=False)
    cve_record: Mapped["CVERecord"] = relationship(back_populates="cna_container")
    
    def __repr__(self) -> str:
        return f"<CnaContainer(id={self.id}, title={self.title[:30]}...)>"

    @classmethod
    def make_from_json(cls, data: dict, cve_record: CVERecord):
        """asad"""
        
        # print(f"\n\n*** CnaContainer :: make_from_json :: data = {data}")
        # print(f"\n descriptions = {data['descriptions']}")
        descriptions = data.get('descriptions')
        
        if date_assigned := data.get('dateAssigned'):
            date_assigned = datetime.fromisoformat(date_assigned)
        
        if date_public := data.get('datePublic'):
            date_public = datetime.fromisoformat(date_public)
        
        return cls(
            title=data.get('title'),
            description=descriptions[0].get('value') if descriptions else "null",
            date_assigned=date_assigned,
            date_public=date_public,
            cve_record=cve_record
        )


class AdpContainer(Base):
    __tablename__ = "adp_containers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=256), nullable=True)
    description: Mapped[str] = mapped_column(String(length=4096), nullable=True)
    date_assigned: Mapped[datetime] = mapped_column(Date(), nullable=True)
    date_public: Mapped[datetime] = mapped_column(Date(), nullable=True)
    
    cve_record_id: Mapped[str] = mapped_column(ForeignKey("cves.id"), nullable=False)
    cve_record: Mapped["CVERecord"] = relationship(back_populates="adp_containers")

    def __repr__(self) -> str:
        return f"<AdpContainer(id={self.id}, title={self.title[:30]}...)>"

    @classmethod
    def make_from_json(cls, data: dict, cve_record: CVERecord):
        """asad"""
        
        if date_assigned := data.get('dateAssigned'):
            date_assigned = datetime.fromisoformat(date_assigned)
        
        if date_public := data.get('datePublic'):
            date_public = datetime.fromisoformat(date_public)
        
        descriptions = data.get('descriptions')
        return cls(
            title=data['title'],
            description=descriptions[0].get('value') if descriptions else "null",
            date_assigned=date_assigned,
            date_public=date_public,
            cve_record=cve_record
        )