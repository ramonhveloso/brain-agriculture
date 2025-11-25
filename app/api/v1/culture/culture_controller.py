from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.api.v1.culture.culture_repository import CultureRepository
from app.api.v1.culture.culture_schemas import (
    CreateCultureRequest,
    CreateCultureResponse,
    DeleteCultureResponse,
    GetCultureResponse,
    GetCulturesResponse,
    UpdateCultureRequest,
    UpdateCultureResponse
)
from app.api.v1.culture.culture_service import CultureService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
service = CultureService(CultureRepository())


@router.get("/")
async def get_cultures(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetCulturesResponse:
    response = await service.get_all(db)
    return GetCulturesResponse.model_validate(response)


@router.get("/{culture_id}")
async def get_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    culture_id: int,
    db: Session = Depends(get_db),
) -> GetCultureResponse:
    response = await service.get_by_id(db, culture_id)
    return GetCultureResponse.model_validate(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: CreateCultureRequest,
    db: Session = Depends(get_db),
) -> CreateCultureResponse:
    response = await service.create(db, data)
    return CreateCultureResponse.model_validate(response)


@router.put("/{culture_id}")
async def put_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    culture_id: int,
    data: UpdateCultureRequest,
    db: Session = Depends(get_db),
) -> UpdateCultureResponse:
    response = await service.update(db, culture_id, data)
    return UpdateCultureResponse.model_validate(response)


@router.delete("/{culture_id}")
async def delete_culture(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    culture_id: int,
    db: Session = Depends(get_db),
) -> DeleteCultureResponse:
    response = await service.delete(db, culture_id)
    return DeleteCultureResponse.model_validate(response)
