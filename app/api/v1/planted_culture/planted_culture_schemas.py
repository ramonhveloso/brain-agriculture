from typing import List, Optional

from pydantic import BaseModel


class CreatePlantedCultureRequest(BaseModel):
    propriedade_safra_id: int
    cultura_id: int

    class Config:
        from_attributes = True


class CreatePlantedCultureResponse(BaseModel):
    id: int
    propriedade_safra_id: int
    cultura_id: int

    class Config:
        from_attributes = True


class PlantedCulture(BaseModel):
    id: int
    propriedade_safra_id: int
    cultura_id: int

    class Config:
        from_attributes = True


class GetPlantedCulturesResponse(BaseModel):
    planted_cultures: List[PlantedCulture]

    class Config:
        from_attributes = True


class GetPlantedCultureResponse(BaseModel):
    id: int
    propriedade_safra_id: int
    cultura_id: int

    class Config:
        from_attributes = True


class UpdatePlantedCultureRequest(BaseModel):
    propriedade_safra_id: Optional[int] = None
    cultura_id: Optional[int] = None

    class Config:
        from_attributes = True


class UpdatePlantedCultureResponse(BaseModel):
    id: int
    propriedade_safra_id: int
    cultura_id: int

    class Config:
        from_attributes = True


class DeletePlantedCultureResponse(BaseModel):
    id: int
    propriedade_safra_id: int
    cultura_id: int

    class Config:
        from_attributes = True
