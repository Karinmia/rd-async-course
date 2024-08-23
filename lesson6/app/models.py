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
    __table_args__ = (
        CheckConstraint("id ~ '^CVE-[0-9]{4}-[0-9]{4,19}$'", name='valid_cve_id'),
    )

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
        unique=True,
        server_default=func.gen_random_uuid(),
        comment="The UUID for the organization to which the CVE ID was originally assigned."
    )
    assigner_short_name: Mapped[str] = mapped_column(String(length=32), nullable=False,)
    date_reserved: Mapped[datetime] = mapped_column(Date(), nullable=False, server_default=func.now())
    date_published: Mapped[datetime] = mapped_column(Date(), nullable=False, server_default=func.now())
    date_updated: Mapped[datetime] = mapped_column(
        Date(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    cna_container: Mapped["CnaContainer"] = relationship(back_populates="cve_record")
    adp_container: Mapped["AdpContainer"] = relationship(back_populates="cve_record")

    def __repr__(self) -> str:
        return f"<CVERecord(id={self.id})>"


class CnaContainer(Base):
    __tablename__ = "cna_containers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    title: Mapped[str] = mapped_column(
        String(length=256),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(length=4096),
        nullable=False,
    )
    date_assigned: Mapped[datetime] = mapped_column(Date(), server_default=func.now())
    date_public: Mapped[datetime] = mapped_column(Date(), server_default=func.now())

    cve_record_id: Mapped[str] = mapped_column(ForeignKey("cves.id"), nullable=False)
    cve_record: Mapped["CVERecord"] = relationship(back_populates="cna_container")
    
    def __repr__(self) -> str:
        return f"<CnaContainer(id={self.id}, title={self.title[:30]}...)>"


class AdpContainer(Base):
    __tablename__ = "adp_containers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    title: Mapped[str] = mapped_column(
        String(length=256),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(length=4096),
        nullable=False,
    )
    date_assigned: Mapped[datetime] = mapped_column(Date(), server_default=func.now())
    date_public: Mapped[datetime] = mapped_column(Date(), server_default=func.now())
    
    cve_record_id: Mapped[str] = mapped_column(ForeignKey("cves.id"), nullable=False)
    cve_record: Mapped["CVERecord"] = relationship(back_populates="adp_container")

    def __repr__(self) -> str:
        return f"<AdpContainer(id={self.id}, title={self.title[:30]}...)>"
