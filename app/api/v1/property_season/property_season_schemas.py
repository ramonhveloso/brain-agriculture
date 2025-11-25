from typing import List, Optional

from pydantic import BaseModel


class CreatePropertySeasonRequest(BaseModel):
    propriedade_id: int
    safra_id: int

    class Config:
        from_attributes = True


class PropertySeason(BaseModel):
    id: int
    propriedade_id: int
    safra_id: int

    class Config:
        from_attributes = True


class CreatePropertySeasonResponse(BaseModel):
    id: int
    propriedade_id: int
    safra_id: int

    class Config:
        from_attributes = True


class GetPropertySeasonResponse(PropertySeason):
    pass


class GetPropertySeasonsResponse(BaseModel):
    seasons: List[PropertySeason]

    class Config:
        from_attributes = True


class UpdatePropertySeasonRequest(BaseModel):
    propriedade_id: Optional[int] = None
    safra_id: Optional[int] = None

    class Config:
        from_attributes = True


class UpdatePropertySeasonResponse(PropertySeason):
    pass


class DeletePropertySeasonResponse(PropertySeason):
    pass
