from sqlalchemy.orm import Session

from app.api.v1.season.season_schemas import (PostSeasonRequest,
                                              PutSeasonRequest)
from app.database.models.season import Season


class SeasonRepository:

    async def get_all(self, db: Session):
        return db.query(Season).all()

    async def get_by_id(self, db: Session, season_id: int):
        return db.query(Season).filter(Season.id == season_id).first()

    async def get_by_name(self, db: Session, nome: str):
        return db.query(Season).filter(Season.nome == nome).first()

    async def create(self, db: Session, data: PostSeasonRequest):
        season = Season(
            nome=data.nome,
            ano=data.ano,
        )
        db.add(season)
        db.commit()
        db.refresh(season)
        return season

    async def update(self, db: Session, season: Season, data: PutSeasonRequest):
        season.nome = data.nome or season.nome
        season.ano = data.ano or season.ano
        db.commit()
        db.refresh(season)
        return season

    async def delete(self, db: Session, season: Season):
        db.delete(season)
        db.commit()
        return season
