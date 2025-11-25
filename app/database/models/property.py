from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.audit_mixin import AuditMixin


class Property(Base, AuditMixin):
    __tablename__ = "propriedades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    produtor_id: Mapped[int] = mapped_column(
        ForeignKey("produtores.id", ondelete="CASCADE")
    )

    nome_fazenda: Mapped[str] = mapped_column(String(150))
    cidade: Mapped[str] = mapped_column(String(120))
    estado: Mapped[str] = mapped_column(String(2))

    area_total: Mapped[float] = mapped_column(Numeric(12, 2))
    area_agricultavel: Mapped[float] = mapped_column(Numeric(12, 2))
    area_vegetacao: Mapped[float] = mapped_column(Numeric(12, 2))

    __table_args__ = (
        CheckConstraint(
            "area_agricultavel + area_vegetacao <= area_total",
            name="ck_soma_area_menor_igual_total",
        ),
    )

    produtor = relationship("Producer", back_populates="propriedades")
    propriedades_safra = relationship("PropertySeason", back_populates="propriedade")
