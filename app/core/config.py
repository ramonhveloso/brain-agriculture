import os

from dotenv import load_dotenv


class Settings:
    PROJECT_NAME: str = "ERP Project Backend"

    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL is None:
        raise ValueError("A variável de ambiente DATABASE_URL não está definida.")


settings = Settings()
