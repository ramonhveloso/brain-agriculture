from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.property_season.property_season_repository import \
    PropertySeasonRepository
from app.api.v1.property_season.property_season_schemas import (
    CreatePropertySeasonRequest, CreatePropertySeasonResponse,
    DeletePropertySeasonResponse, GetPropertySeasonResponse,
    GetPropertySeasonsResponse, PropertySeason, UpdatePropertySeasonRequest,
    UpdatePropertySeasonResponse)
from app.database.models.property import Property
from app.database.models.season import Season


class PropertySeasonService:
    def __init__(self, repository: PropertySeasonRepository = Depends()):
        self.repo = repository

    async def get_all(self, db: Session) -> GetPropertySeasonsResponse:
        entries = await self.repo.get_all(db)
        return GetPropertySeasonsResponse(
            seasons=[PropertySeason.model_validate(e) for e in entries]
        )

    async def get_by_id(self, db: Session, season_id: int) -> GetPropertySeasonResponse:
        entry = await self.repo.get_by_id(db, season_id)
        if not entry:
            raise HTTPException(status_code=404, detail="PropertySeason not found")
        return GetPropertySeasonResponse.model_validate(entry)

    async def create(self, db: Session, data: CreatePropertySeasonRequest):
        if not db.query(Property).filter(Property.id == data.propriedade_id).first():
            raise HTTPException(status_code=400, detail="Property does not exist")

        if not db.query(Season).filter(Season.id == data.safra_id).first():
            raise HTTPException(status_code=400, detail="Season does not exist")

        if await self.repo.get_existing_relation(
            db, data.propriedade_id, data.safra_id
        ):
            raise HTTPException(
                status_code=400, detail="This property is already linked to this season"
            )

        created = await self.repo.create(db, data)
        return CreatePropertySeasonResponse.model_validate(created)

    async def update(
        self, db: Session, season_id: int, data: UpdatePropertySeasonRequest
    ):
        season = await self.repo.get_by_id(db, season_id)
        if not season:
            raise HTTPException(status_code=404, detail="PropertySeason not found")

        updated = await self.repo.update(db, season, data)
        return UpdatePropertySeasonResponse.model_validate(updated)

    async def delete(self, db: Session, season_id: int):
        season = await self.repo.get_by_id(db, season_id)
        if not season:
            raise HTTPException(status_code=404, detail="PropertySeason not found")

        deleted = await self.repo.delete(db, season)
        return DeletePropertySeasonResponse.model_validate(deleted)
