from fastapi import APIRouter

from app.api.v1.auth.auth_controller import router as auth_router
from app.api.v1.culture.culture_controller import router as cultures_router
from app.api.v1.planted_culture.planted_culture_controller import \
    router as planted_cultures_router
from app.api.v1.producer.producer_controller import router as producers_router
from app.api.v1.property.property_controller import router as properties_router
from app.api.v1.property_season.property_season_controller import \
    router as property_seasons_router
from app.api.v1.season.season_controller import router as seasons_router
from app.api.v1.user.user_controller import router as users_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(producers_router, prefix="/producers", tags=["Producers"])
router.include_router(properties_router, prefix="/properties", tags=["Properties"])
router.include_router(seasons_router, prefix="/seasons", tags=["Seasons"])
router.include_router(
    property_seasons_router, prefix="/property-seasons", tags=["Property Seasons"]
)
router.include_router(cultures_router, prefix="/cultures", tags=["Cultures"])
router.include_router(
    planted_cultures_router, prefix="/planted-cultures", tags=["Planted Cultures"]
)
