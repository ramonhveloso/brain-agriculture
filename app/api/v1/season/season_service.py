from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.season.season_repository import SeasonRepository
from app.api.v1.season.season_schemas import (DeleteSeasonResponse,
                                              GetSeasonResponse,
                                              GetSeasonsResponse,
                                              PostSeasonRequest,
                                              PostSeasonResponse,
                                              PutSeasonRequest,
                                              PutSeasonResponse, Season)


class SeasonService:
    def __init__(self, repository: SeasonRepository = Depends()):
        self.repository = repository

    async def get_all(self, db: Session) -> GetSeasonsResponse:
        seasons = await self.repository.get_all(db)
        items = [Season.model_validate(s) for s in seasons]
        return GetSeasonsResponse(seasons=items)

    async def get_by_id(self, db: Session, season_id: int) -> GetSeasonResponse:
        season = await self.repository.get_by_id(db, season_id)
        if not season:
            raise HTTPException(status_code=404, detail="Season não encontrada")
        return GetSeasonResponse.model_validate(season)

    async def create(self, db: Session, data: PostSeasonRequest) -> PostSeasonResponse:
        existing = await self.repository.get_by_name(db, data.nome)
        if existing:
            raise HTTPException(status_code=400, detail="Season já cadastrada")

        season = await self.repository.create(db, data)
        return PostSeasonResponse.model_validate(season)

    async def update(
        self, db: Session, season_id: int, data: PutSeasonRequest
    ) -> PutSeasonResponse:
        season = await self.repository.get_by_id(db, season_id)
        if not season:
            raise HTTPException(status_code=404, detail="Season não encontrada")

        updated = await self.repository.update(db, season, data)
        return PutSeasonResponse.model_validate(updated)

    async def delete(self, db: Session, season_id: int) -> DeleteSeasonResponse:
        season = await self.repository.get_by_id(db, season_id)
        if not season:
            raise HTTPException(status_code=404, detail="Season não encontrada")

        deleted = await self.repository.delete(db, season)
        return DeleteSeasonResponse.model_validate(deleted)
