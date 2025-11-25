from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.api.v1.planted_culture.planted_culture_repository import \
    PlantedCultureRepository
from app.api.v1.planted_culture.planted_culture_schemas import (
    CreatePlantedCultureRequest, CreatePlantedCultureResponse,
    DeletePlantedCultureResponse, GetPlantedCultureResponse,
    GetPlantedCulturesResponse, UpdatePlantedCultureRequest,
    UpdatePlantedCultureResponse)
from app.api.v1.planted_culture.planted_culture_service import \
    PlantedCultureService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
service = PlantedCultureService(PlantedCultureRepository())


@router.get("/")
async def get_planted_cultures(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetPlantedCulturesResponse:
    response = await service.get_all(db)
    return GetPlantedCulturesResponse.model_validate(response)


@router.get("/{planted_culture_id}")
async def get_planted_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    planted_culture_id: int,
    db: Session = Depends(get_db),
) -> GetPlantedCultureResponse:
    response = await service.get_by_id(db, planted_culture_id)
    return GetPlantedCultureResponse.model_validate(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_planted_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: CreatePlantedCultureRequest,
    db: Session = Depends(get_db),
) -> CreatePlantedCultureResponse:
    response = await service.create(db, data)
    return CreatePlantedCultureResponse.model_validate(response)


@router.put("/{planted_culture_id}")
async def put_planted_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    planted_culture_id: int,
    data: UpdatePlantedCultureRequest,
    db: Session = Depends(get_db),
) -> UpdatePlantedCultureResponse:
    response = await service.update(db, planted_culture_id, data)
    return UpdatePlantedCultureResponse.model_validate(response)


@router.delete("/{planted_culture_id}")
async def delete_planted_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    planted_culture_id: int,
    db: Session = Depends(get_db),
) -> DeletePlantedCultureResponse:
    response = await service.delete(db, planted_culture_id)
    return DeletePlantedCultureResponse.model_validate(response)
