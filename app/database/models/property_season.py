from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.audit_mixin import AuditMixin


class PropertySeason(Base, AuditMixin):
    __tablename__ = "propriedade_safra"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    propriedade_id: Mapped[int] = mapped_column(
        ForeignKey("propriedades.id", ondelete="CASCADE")
    )
    safra_id: Mapped[int] = mapped_column(ForeignKey("safras.id"))

    __table_args__ = (
        UniqueConstraint("propriedade_id", "safra_id", name="uq_propriedade_safra"),
    )

    propriedade = relationship("Property", back_populates="propriedades_safra")
    safra = relationship("Season", back_populates="propriedades_safra")
    culturas_plantadas = relationship(
        "PlantedCulture", back_populates="propriedade_safra"
    )
