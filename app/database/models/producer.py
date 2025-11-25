from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.audit_mixin import AuditMixin


class Producer(Base, AuditMixin):
    __tablename__ = "produtores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cpf_cnpj: Mapped[str] = mapped_column(String(20), unique=True)
    nome_produtor: Mapped[str] = mapped_column(String(150))

    propriedades = relationship("Property", back_populates="produtor")
