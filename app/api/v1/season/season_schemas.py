from typing import List, Optional

from pydantic import BaseModel


class PostSeasonRequest(BaseModel):
    nome: str
    ano: int

    class Config:
        from_attributes = True


class PostSeasonResponse(BaseModel):
    id: int
    nome: str
    ano: int

    class Config:
        from_attributes = True


class Season(BaseModel):
    id: int
    nome: str
    ano: int

    class Config:
        from_attributes = True


class GetSeasonsResponse(BaseModel):
    seasons: List[Season]

    class Config:
        from_attributes = True


class GetSeasonResponse(BaseModel):
    id: int
    nome: str
    ano: int

    class Config:
        from_attributes = True


class PutSeasonRequest(BaseModel):
    nome: Optional[str] = None
    ano: Optional[int] = None

    class Config:
        from_attributes = True


class PutSeasonResponse(BaseModel):
    id: int
    nome: str
    ano: int

    class Config:
        from_attributes = True


class DeleteSeasonResponse(BaseModel):
    id: int
    nome: str
    ano: int

    class Config:
        from_attributes = True
