from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.property.property_repository import PropertyRepository
from app.api.v1.property.property_schemas import (DeletePropertyResponse,
                                                  GetPropertiesResponse,
                                                  GetPropertyResponse,
                                                  PostPropertyRequest,
                                                  PostPropertyResponse,
                                                  Property, PutPropertyRequest,
                                                  PutPropertyResponse)
from app.database.models.producer import Producer


class PropertyService:
    def __init__(self, repository: PropertyRepository = Depends()):
        self.repository = repository

    async def get_all(self, db: Session) -> GetPropertiesResponse:
        items = await self.repository.get_all(db)
        return GetPropertiesResponse(
            properties=[Property.model_validate(p) for p in items]
        )

    async def get_by_id(self, db: Session, property_id: int) -> GetPropertyResponse:
        entity = await self.repository.get_by_id(db, property_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Property not found")
        return GetPropertyResponse.model_validate(entity)

    async def create(
        self, db: Session, data: PostPropertyRequest
    ) -> PostPropertyResponse:
        produtor = db.query(Producer).filter(Producer.id == data.produtor_id).first()
        if not produtor:
            raise HTTPException(status_code=400, detail="Producer does not exist")

        entity = await self.repository.create(db, data)
        return PostPropertyResponse.model_validate(entity)

    async def update(
        self, db: Session, property_id: int, data: PutPropertyRequest
    ) -> PutPropertyResponse:
        entity = await self.repository.get_by_id(db, property_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Property not found")

        entity = await self.repository.update(db, entity, data)
        return PutPropertyResponse.model_validate(entity)

    async def delete(self, db: Session, property_id: int) -> DeletePropertyResponse:
        entity = await self.repository.get_by_id(db, property_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Property not found")

        deleted = await self.repository.delete(db, entity)
        return DeletePropertyResponse.model_validate(deleted)
