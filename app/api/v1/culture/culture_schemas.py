from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CreateCultureRequest(BaseModel):
    nome: str

    model_config = ConfigDict(from_attributes=True)
    

class CreateCultureResponse(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class Culture(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class GetCulturesResponse(BaseModel):
    cultures: List[Culture]

    model_config = ConfigDict(from_attributes=True)


class GetCultureResponse(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class UpdateCultureRequest(BaseModel):
    nome: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateCultureResponse(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class DeleteCultureResponse(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)
        
