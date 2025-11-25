from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.api.v1.property_season.property_season_repository import \
    PropertySeasonRepository
from app.api.v1.property_season.property_season_schemas import (
    CreatePropertySeasonRequest, CreatePropertySeasonResponse,
    DeletePropertySeasonResponse, GetPropertySeasonResponse,
    GetPropertySeasonsResponse, UpdatePropertySeasonRequest,
    UpdatePropertySeasonResponse)
from app.api.v1.property_season.property_season_service import \
    PropertySeasonService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
service = PropertySeasonService(PropertySeasonRepository())


@router.get("/")
async def get_property_seasons(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetPropertySeasonsResponse:
    response = await service.get_all(db)
    return GetPropertySeasonsResponse.model_validate(response)


@router.get("/{season_id}")
async def get_property_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    season_id: int,
    db: Session = Depends(get_db),
) -> GetPropertySeasonResponse:
    response = await service.get_by_id(db, season_id)
    return GetPropertySeasonResponse.model_validate(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_property_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: CreatePropertySeasonRequest,
    db: Session = Depends(get_db),
) -> CreatePropertySeasonResponse:
    response = await service.create(db, data)
    return CreatePropertySeasonResponse.model_validate(response)


@router.put("/{season_id}")
async def update_property_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    season_id: int,
    data: UpdatePropertySeasonRequest,
    db: Session = Depends(get_db),
) -> UpdatePropertySeasonResponse:
    response = await service.update(db, season_id, data)
    return UpdatePropertySeasonResponse.model_validate(response)


@router.delete("/{season_id}")
async def delete_property_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    season_id: int,
    db: Session = Depends(get_db),
) -> DeletePropertySeasonResponse:
    response = await service.delete(db, season_id)
    return DeletePropertySeasonResponse.model_validate(response)
