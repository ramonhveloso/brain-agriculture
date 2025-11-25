from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.api.v1.season.season_repository import SeasonRepository
from app.api.v1.season.season_schemas import (DeleteSeasonResponse,
                                              GetSeasonResponse,
                                              GetSeasonsResponse,
                                              PostSeasonRequest,
                                              PostSeasonResponse,
                                              PutSeasonRequest,
                                              PutSeasonResponse)
from app.api.v1.season.season_service import SeasonService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
service = SeasonService(SeasonRepository())


@router.get("/")
async def get_seasons(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetSeasonsResponse:
    response = await service.get_all(db)
    return GetSeasonsResponse.model_validate(response)


@router.get("/{season_id}")
async def get_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    season_id: int,
    db: Session = Depends(get_db),
) -> GetSeasonResponse:
    response = await service.get_by_id(db, season_id)
    return GetSeasonResponse.model_validate(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: PostSeasonRequest,
    db: Session = Depends(get_db),
) -> PostSeasonResponse:
    response = await service.create(db, data)
    return PostSeasonResponse.model_validate(response)


@router.put("/{season_id}")
async def put_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    season_id: int,
    data: PutSeasonRequest,
    db: Session = Depends(get_db),
) -> PutSeasonResponse:
    response = await service.update(db, season_id, data)
    return PutSeasonResponse.model_validate(response)


@router.delete("/{season_id}")
async def delete_season(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    season_id: int,
    db: Session = Depends(get_db),
) -> DeleteSeasonResponse:
    response = await service.delete(db, season_id)
    return DeleteSeasonResponse.model_validate(response)
