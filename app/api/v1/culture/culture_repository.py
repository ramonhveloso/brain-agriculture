from sqlalchemy.orm import Session

from app.api.v1.culture.culture_schemas import (CreateCultureRequest,
                                                UpdateCultureRequest)
from app.database.models.culture import Culture


class CultureRepository:
    async def get_all(self, db: Session):
        return db.query(Culture).all()

    async def get_by_id(self, db: Session, culture_id: int):
        return db.query(Culture).filter(Culture.id == culture_id).first()

    async def get_by_name(self, db: Session, nome: str):
        return db.query(Culture).filter(Culture.nome == nome).first()

    async def create(self, db: Session, data: CreateCultureRequest):
        culture = Culture(nome=data.nome)
        db.add(culture)
        db.commit()
        db.refresh(culture)
        return culture

    async def update(self, db: Session, culture: Culture, data: UpdateCultureRequest):
        culture.nome = data.nome or culture.nome
        db.commit()
        db.refresh(culture)
        return culture

    async def delete(self, db: Session, culture: Culture):
        db.delete(culture)
        db.commit()
        return culture
