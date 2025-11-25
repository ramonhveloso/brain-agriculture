from typing import List, Optional

from pydantic import BaseModel


class CreateCultureRequest(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class CreateCultureResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class Culture(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class GetCulturesResponse(BaseModel):
    cultures: List[Culture]

    class Config:
        from_attributes = True


class GetCultureResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class UpdateCultureRequest(BaseModel):
    nome: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateCultureResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class DeleteCultureResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True
