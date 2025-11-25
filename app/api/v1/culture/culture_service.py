from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.culture.culture_repository import CultureRepository
from app.api.v1.culture.culture_schemas import (CreateCultureRequest,
                                                CreateCultureResponse, Culture,
                                                DeleteCultureResponse,
                                                GetCultureResponse,
                                                GetCulturesResponse,
                                                UpdateCultureRequest,
                                                UpdateCultureResponse)


class CultureService:
    def __init__(self, repository: CultureRepository = Depends()):
        self.repository = repository

    async def get_all(self, db: Session) -> GetCulturesResponse:
        cultures = await self.repository.get_all(db)
        items = [Culture.model_validate(c) for c in cultures]
        return GetCulturesResponse(cultures=items)

    async def get_by_id(self, db: Session, culture_id: int) -> GetCultureResponse:
        culture = await self.repository.get_by_id(db, culture_id)
        if not culture:
            raise HTTPException(status_code=404, detail="Culture not found")
        return GetCultureResponse.model_validate(culture)

    async def create(
        self, db: Session, data: CreateCultureRequest
    ) -> CreateCultureResponse:
        existing = await self.repository.get_by_name(db, data.nome)
        if existing:
            raise HTTPException(status_code=400, detail="Culture already exists")

        culture = await self.repository.create(db, data)
        return CreateCultureResponse.model_validate(culture)

    async def update(
        self, db: Session, culture_id: int, data: UpdateCultureRequest
    ) -> UpdateCultureResponse:
        culture = await self.repository.get_by_id(db, culture_id)
        if not culture:
            raise HTTPException(status_code=404, detail="Culture not found")

        culture = await self.repository.update(db, culture, data)
        return UpdateCultureResponse.model_validate(culture)

    async def delete(self, db: Session, culture_id: int) -> DeleteCultureResponse:
        culture = await self.repository.get_by_id(db, culture_id)
        if not culture:
            raise HTTPException(status_code=404, detail="Culture not found")

        deleted = await self.repository.delete(db, culture)
        return DeleteCultureResponse.model_validate(deleted)
