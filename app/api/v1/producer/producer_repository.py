from sqlalchemy.orm import Session

from app.api.v1.producer.producer_schemas import (CreateProducerRequest,
                                                  UpdateProducerRequest)
from app.database.models.producer import Producer


class ProducerRepository:

    async def get_all(self, db: Session):
        return db.query(Producer).filter(Producer.excluido_em.is_(None)).all()

    async def get_by_id(self, db: Session, producer_id: int):
        return (
            db.query(Producer)
            .filter(Producer.id == producer_id, Producer.excluido_em.is_(None))
            .first()
        )

    async def get_by_cpf_cnpj(self, db: Session, cpf_cnpj: str):
        return db.query(Producer).filter(Producer.cpf_cnpj == cpf_cnpj).first()

    async def create(self, db: Session, data: CreateProducerRequest):
        producer = Producer(
            cpf_cnpj=data.cpf_cnpj,
            nome_produtor=data.nome_produtor,
        )
        db.add(producer)
        db.commit()
        db.refresh(producer)
        return producer

    async def update(
        self, db: Session, producer: Producer, data: UpdateProducerRequest
    ):
        if data.cpf_cnpj:
            producer.cpf_cnpj = data.cpf_cnpj
        if data.nome_produtor:
            producer.nome_produtor = data.nome_produtor

        db.commit()
        db.refresh(producer)
        return producer

    async def soft_delete(self, db: Session, producer: Producer, user_id: int):
        from datetime import datetime, timezone

        producer.excluido_em = datetime.now(timezone.utc)
        producer.excluido_por = user_id
        db.commit()
        db.refresh(producer)
        return producer
