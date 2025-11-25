from sqlalchemy.orm import Session

from app.api.v1.planted_culture.planted_culture_schemas import (
    CreatePlantedCultureRequest, UpdatePlantedCultureRequest)
from app.database.models.planted_culture import PlantedCulture


class PlantedCultureRepository:
    async def get_all(self, db: Session):
        return db.query(PlantedCulture).all()

    async def get_by_id(self, db: Session, planted_culture_id: int):
        return (
            db.query(PlantedCulture)
            .filter(PlantedCulture.id == planted_culture_id)
            .first()
        )

    async def get_by_unique(
        self, db: Session, propriedade_safra_id: int, cultura_id: int
    ):
        return (
            db.query(PlantedCulture)
            .filter(
                PlantedCulture.propriedade_safra_id == propriedade_safra_id,
                PlantedCulture.cultura_id == cultura_id,
            )
            .first()
        )

    async def create(self, db: Session, data: CreatePlantedCultureRequest):
        record = PlantedCulture(
            propriedade_safra_id=data.propriedade_safra_id,
            cultura_id=data.cultura_id,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    async def update(
        self, db: Session, record: PlantedCulture, data: UpdatePlantedCultureRequest
    ):
        record.propriedade_safra_id = (
            data.propriedade_safra_id or record.propriedade_safra_id
        )
        record.cultura_id = data.cultura_id or record.cultura_id
        db.commit()
        db.refresh(record)
        return record

    async def delete(self, db: Session, record: PlantedCulture):
        db.delete(record)
        db.commit()
        return record
