from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.audit_mixin import AuditMixin


class Season(Base, AuditMixin):
    __tablename__ = "safras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True)
    ano: Mapped[int] = mapped_column(Integer)

    propriedades_safra = relationship("PropertySeason", back_populates="safra")
