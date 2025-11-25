from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.audit_mixin import AuditMixin


class PlantedCulture(Base, AuditMixin):
    __tablename__ = "cultura_plantada"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    propriedade_safra_id: Mapped[int] = mapped_column(
        ForeignKey("propriedade_safra.id", ondelete="CASCADE")
    )
    cultura_id: Mapped[int] = mapped_column(
        ForeignKey("culturas.id", ondelete="CASCADE")
    )

    __table_args__ = (
        UniqueConstraint(
            "propriedade_safra_id", "cultura_id", name="uq_cultura_plantada"
        ),
    )

    propriedade_safra = relationship(
        "PropertySeason", back_populates="culturas_plantadas"
    )
    cultura = relationship("Culture", back_populates="culturas_plantadas")
