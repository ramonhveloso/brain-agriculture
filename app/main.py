from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.logging.config import setup_logging
from app.database.base import Base
from app.database.session import engine
from app.middleware.logging_middleware import logging_middleware

setup_logging()

app = FastAPI(
    title="Brain Agriculture",
    description="Teste https://github.com/brain-ag/trabalhe-conosco Brain Agriculture",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")
app.middleware("http")(logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8007)
