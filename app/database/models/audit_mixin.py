from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column


class AuditMixin:
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    criado_por: Mapped[int | None] = mapped_column(Integer, nullable=True)

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    atualizado_por: Mapped[int | None] = mapped_column(Integer, nullable=True)

    excluido_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    excluido_por: Mapped[int | None] = mapped_column(Integer, nullable=True)
