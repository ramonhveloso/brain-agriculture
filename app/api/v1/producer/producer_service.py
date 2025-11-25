from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.producer.producer_repository import ProducerRepository
from app.api.v1.producer.producer_schemas import (CreateProducerRequest,
                                                  CreateProducerResponse,
                                                  DeleteProducerResponse,
                                                  GetProducerResponse,
                                                  GetProducersResponse,
                                                  Producer,
                                                  UpdateProducerRequest,
                                                  UpdateProducerResponse)


class ProducerService:
    def __init__(self, repository: ProducerRepository = Depends()):
        self.repository = repository

    async def get_all(self, db: Session) -> GetProducersResponse:
        producers = await self.repository.get_all(db)
        items = [Producer.model_validate(p) for p in producers]
        return GetProducersResponse(producers=items)

    async def get_by_id(self, db: Session, producer_id: int) -> GetProducerResponse:
        producer = await self.repository.get_by_id(db, producer_id)
        if not producer:
            raise HTTPException(status_code=404, detail="Producer not found")
        return GetProducerResponse.model_validate(producer)

    async def create(
        self, db: Session, data: CreateProducerRequest
    ) -> CreateProducerResponse:
        existing = await self.repository.get_by_cpf_cnpj(db, data.cpf_cnpj)
        if existing:
            raise HTTPException(status_code=400, detail="CPF/CNPJ already registered")

        created = await self.repository.create(db, data)
        return CreateProducerResponse.model_validate(created)

    async def update(self, db: Session, producer_id: int, data: UpdateProducerRequest):
        producer = await self.repository.get_by_id(db, producer_id)
        if not producer:
            raise HTTPException(status_code=404, detail="Producer not found")

        updated = await self.repository.update(db, producer, data)
        return UpdateProducerResponse.model_validate(updated)

    async def delete(self, db: Session, producer_id: int, user_id: int):
        producer = await self.repository.get_by_id(db, producer_id)
        if not producer:
            raise HTTPException(status_code=404, detail="Producer not found")

        deleted = await self.repository.soft_delete(db, producer, user_id)
        return DeleteProducerResponse.model_validate(deleted)
