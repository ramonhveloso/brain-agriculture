from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.planted_culture.planted_culture_repository import \
    PlantedCultureRepository
from app.api.v1.planted_culture.planted_culture_schemas import (
    CreatePlantedCultureRequest, CreatePlantedCultureResponse,
    DeletePlantedCultureResponse, GetPlantedCultureResponse,
    GetPlantedCulturesResponse, PlantedCulture, UpdatePlantedCultureRequest,
    UpdatePlantedCultureResponse)
from app.database.models.culture import Culture
from app.database.models.property_season import PropertySeason


class PlantedCultureService:
    def __init__(self, repository: PlantedCultureRepository = Depends()):
        self.repository = repository

    async def get_all(self, db: Session) -> GetPlantedCulturesResponse:
        records = await self.repository.get_all(db)
        items = [PlantedCulture.model_validate(r) for r in records]
        return GetPlantedCulturesResponse(planted_cultures=items)

    async def get_by_id(
        self, db: Session, planted_culture_id: int
    ) -> GetPlantedCultureResponse:
        record = await self.repository.get_by_id(db, planted_culture_id)
        if not record:
            raise HTTPException(status_code=404, detail="Planted culture not found")
        return GetPlantedCultureResponse.model_validate(record)

    async def create(
        self, db: Session, data: CreatePlantedCultureRequest
    ) -> CreatePlantedCultureResponse:
        cultura = db.query(Culture).filter(Culture.id == data.cultura_id).first()
        if not cultura:
            raise HTTPException(status_code=404, detail="Culture not found")

        propriedade_safra = (
            db.query(PropertySeason)
            .filter(PropertySeason.id == data.propriedade_safra_id)
            .first()
        )
        if not propriedade_safra:
            raise HTTPException(status_code=404, detail="Property-Season not found")

        existing = await self.repository.get_by_unique(
            db, data.propriedade_safra_id, data.cultura_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Culture already registered for this property-season",
            )

        record = await self.repository.create(db, data)
        return CreatePlantedCultureResponse.model_validate(record)

    async def update(
        self, db: Session, planted_culture_id: int, data: UpdatePlantedCultureRequest
    ) -> UpdatePlantedCultureResponse:
        record = await self.repository.get_by_id(db, planted_culture_id)
        if not record:
            raise HTTPException(status_code=404, detail="Planted culture not found")

        updated = await self.repository.update(db, record, data)
        return UpdatePlantedCultureResponse.model_validate(updated)

    async def delete(
        self, db: Session, planted_culture_id: int
    ) -> DeletePlantedCultureResponse:
        record = await self.repository.get_by_id(db, planted_culture_id)
        if not record:
            raise HTTPException(status_code=404, detail="Planted culture not found")

        deleted = await self.repository.delete(db, record)
        return DeletePlantedCultureResponse.model_validate(deleted)
