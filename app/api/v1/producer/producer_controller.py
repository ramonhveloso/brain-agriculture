from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.api.v1.producer.producer_repository import ProducerRepository
from app.api.v1.producer.producer_schemas import (CreateProducerRequest,
                                                  CreateProducerResponse,
                                                  DeleteProducerResponse,
                                                  GetProducerResponse,
                                                  GetProducersResponse,
                                                  UpdateProducerRequest,
                                                  UpdateProducerResponse)
from app.api.v1.producer.producer_service import ProducerService
from app.core.log import get_logger
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
service = ProducerService(ProducerRepository())
logger = get_logger("Producer")

@router.get("/")
async def get_producers(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetProducersResponse:
    logger.info("get_producers_called", route='/producers', user_id=authuser.id)
    response = await service.get_all(db=db, logger=logger)
    return GetProducersResponse.model_validate(response)


@router.get("/{producer_id}")
async def get_producer(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    producer_id: int,
    db: Session = Depends(get_db),
) -> GetProducerResponse:
    response = await service.get_by_id(db, producer_id)
    return GetProducerResponse.model_validate(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_producer(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: CreateProducerRequest,
    db: Session = Depends(get_db),
) -> CreateProducerResponse:
    response = await service.create(db, data)
    return CreateProducerResponse.model_validate(response)


@router.put("/{producer_id}")
async def update_producer(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    producer_id: int,
    data: UpdateProducerRequest,
    db: Session = Depends(get_db),
) -> UpdateProducerResponse:
    response = await service.update(db, producer_id, data)
    return UpdateProducerResponse.model_validate(response)


@router.delete("/{producer_id}")
async def delete_producer(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    producer_id: int,
    db: Session = Depends(get_db),
) -> DeleteProducerResponse:
    response = await service.delete(db, producer_id, authuser.id)
    return DeleteProducerResponse.model_validate(response)
