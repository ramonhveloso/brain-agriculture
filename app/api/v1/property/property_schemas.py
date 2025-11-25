from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ValidationInfo, field_validator

VALID_STATES = {
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
}


class PostPropertyRequest(BaseModel):
    produtor_id: int
    nome_fazenda: str
    cidade: str
    estado: str
    area_total: Decimal
    area_agricultavel: Decimal
    area_vegetacao: Decimal

    @field_validator("estado")
    def validate_estado(cls, v):
        if v.upper() not in VALID_STATES:
            raise ValueError("Invalid state (UF)")
        return v.upper()

    @field_validator("area_agricultavel", "area_vegetacao")
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError("Areas must be non-negative")
        return v

    @field_validator("area_total")
    def validate_area_total(cls, v):
        if v <= 0:
            raise ValueError("Total area must be greater than zero")
        return v

    @field_validator("area_vegetacao")
    def validate_sum(cls, v, info: ValidationInfo):
        agric = info.data.get("area_agricultavel")
        total = info.data.get("area_total")

        if agric is not None and total is not None:
            if agric + v > total:
                raise ValueError(
                    "Sum of agriculturable + vegetation exceeds total area"
                )
        return v

    class Config:
        from_attributes = True


class Property(BaseModel):
    id: int
    produtor_id: int
    nome_fazenda: str
    cidade: str
    estado: str
    area_total: Decimal
    area_agricultavel: Decimal
    area_vegetacao: Decimal

    class Config:
        from_attributes = True


class PostPropertyResponse(Property):
    pass


class GetPropertyResponse(Property):
    pass


class GetPropertiesResponse(BaseModel):
    properties: List[Property]

    class Config:
        from_attributes = True


class PutPropertyRequest(BaseModel):
    nome_fazenda: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    area_total: Optional[Decimal] = None
    area_agricultavel: Optional[Decimal] = None
    area_vegetacao: Optional[Decimal] = None

    @field_validator("estado")
    def validate_estado(cls, v):
        if v and v.upper() not in VALID_STATES:
            raise ValueError("Invalid state (UF)")
        return v.upper() if v else v

    class Config:
        from_attributes = True


class PutPropertyResponse(Property):
    pass


class DeletePropertyResponse(Property):
    pass
