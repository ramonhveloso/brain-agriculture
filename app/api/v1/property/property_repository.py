from sqlalchemy.orm import Session

from app.api.v1.property.property_schemas import (PostPropertyRequest,
                                                  PutPropertyRequest)
from app.database.models.property import Property


class PropertyRepository:

    async def get_all(self, db: Session):
        return db.query(Property).all()

    async def get_by_id(self, db: Session, property_id: int):
        return db.query(Property).filter(Property.id == property_id).first()

    async def get_by_produtor(self, db: Session, produtor_id: int):
        return db.query(Property).filter(Property.produtor_id == produtor_id).all()

    async def create(self, db: Session, data: PostPropertyRequest):
        entity = Property(
            produtor_id=data.produtor_id,
            nome_fazenda=data.nome_fazenda,
            cidade=data.cidade,
            estado=data.estado,
            area_total=data.area_total,
            area_agricultavel=data.area_agricultavel,
            area_vegetacao=data.area_vegetacao,
        )
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    async def update(self, db: Session, entity: Property, data: PutPropertyRequest):
        if data.nome_fazenda is not None:
            entity.nome_fazenda = data.nome_fazenda

        if data.cidade is not None:
            entity.cidade = data.cidade

        if data.estado is not None:
            entity.estado = data.estado

        entity.area_total = data.area_total or entity.area_total
        entity.area_agricultavel = data.area_agricultavel or entity.area_agricultavel
        entity.area_vegetacao = data.area_vegetacao or entity.area_vegetacao

        if entity.area_agricultavel + entity.area_vegetacao > entity.area_total:
            raise ValueError("Sum of agriculturable + vegetation exceeds total area")

        db.commit()
        db.refresh(entity)
        return entity

    async def delete(self, db: Session, entity: Property):
        db.delete(entity)
        db.commit()
        return entity
