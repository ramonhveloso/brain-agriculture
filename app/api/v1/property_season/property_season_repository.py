from sqlalchemy.orm import Session

from app.api.v1.property_season.property_season_schemas import (
    CreatePropertySeasonRequest, UpdatePropertySeasonRequest)
from app.database.models.property_season import PropertySeason


class PropertySeasonRepository:

    async def get_all(self, db: Session):
        return db.query(PropertySeason).all()

    async def get_by_id(self, db: Session, season_id: int):
        return db.query(PropertySeason).filter(PropertySeason.id == season_id).first()

    async def get_existing_relation(
        self, db: Session, propriedade_id: int, safra_id: int
    ):
        return (
            db.query(PropertySeason)
            .filter(
                PropertySeason.propriedade_id == propriedade_id,
                PropertySeason.safra_id == safra_id,
            )
            .first()
        )

    async def create(self, db: Session, data: CreatePropertySeasonRequest):
        entry = PropertySeason(
            propriedade_id=data.propriedade_id,
            safra_id=data.safra_id,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    async def update(
        self, db: Session, season: PropertySeason, data: UpdatePropertySeasonRequest
    ):
        if data.propriedade_id is not None:
            season.propriedade_id = data.propriedade_id

        if data.safra_id is not None:
            season.safra_id = data.safra_id

        db.commit()
        db.refresh(season)
        return season

    async def delete(self, db: Session, season: PropertySeason):
        db.delete(season)
        db.commit()
        return season
