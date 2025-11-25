from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.audit_mixin import AuditMixin


class Culture(Base, AuditMixin):
    __tablename__ = "culturas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)

    culturas_plantadas = relationship("PlantedCulture", back_populates="cultura")
