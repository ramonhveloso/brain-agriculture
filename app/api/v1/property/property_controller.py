from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.api.v1.property.property_repository import PropertyRepository
from app.api.v1.property.property_schemas import (DeletePropertyResponse,
                                                  GetPropertiesResponse,
                                                  GetPropertyResponse,
                                                  PostPropertyRequest,
                                                  PostPropertyResponse,
                                                  PutPropertyRequest,
                                                  PutPropertyResponse)
from app.api.v1.property.property_service import PropertyService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
service = PropertyService(PropertyRepository())


@router.get("/")
async def get_properties(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetPropertiesResponse:
    response = await service.get_all(db)
    return GetPropertiesResponse.model_validate(response)


@router.get("/{property_id}")
async def get_property(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    property_id: int,
    db: Session = Depends(get_db),
) -> GetPropertyResponse:
    response = await service.get_by_id(db, property_id)
    return GetPropertyResponse.model_validate(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_property(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: PostPropertyRequest,
    db: Session = Depends(get_db),
) -> PostPropertyResponse:
    response = await service.create(db, data)
    return PostPropertyResponse.model_validate(response)


@router.put("/{property_id}")
async def update_property(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    property_id: int,
    data: PutPropertyRequest,
    db: Session = Depends(get_db),
) -> PutPropertyResponse:
    response = await service.update(db, property_id, data)
    return PutPropertyResponse.model_validate(response)


@router.delete("/{property_id}")
async def delete_property(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    property_id: int,
    db: Session = Depends(get_db),
) -> DeletePropertyResponse:
    response = await service.delete(db, property_id)
    return DeletePropertyResponse.model_validate(response)
