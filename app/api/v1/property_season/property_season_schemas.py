from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CreatePropertySeasonRequest(BaseModel):
    propriedade_id: int
    safra_id: int

    model_config = ConfigDict(from_attributes=True)
        

class PropertySeason(BaseModel):
    id: int
    propriedade_id: int
    safra_id: int

    model_config = ConfigDict(from_attributes=True)
        

class CreatePropertySeasonResponse(BaseModel):
    id: int
    propriedade_id: int
    safra_id: int

    model_config = ConfigDict(from_attributes=True)
        

class GetPropertySeasonResponse(PropertySeason):
    pass


class GetPropertySeasonsResponse(BaseModel):
    seasons: List[PropertySeason]

    model_config = ConfigDict(from_attributes=True)
        

class UpdatePropertySeasonRequest(BaseModel):
    propriedade_id: Optional[int] = None
    safra_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
        

class UpdatePropertySeasonResponse(PropertySeason):
    pass


class DeletePropertySeasonResponse(PropertySeason):
    pass
