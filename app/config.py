from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # prod | dev
    ENV: str = "prod"

    # Railway uchun (agar mavjud bo‘lsa)
    DATABASE_URL: Optional[str] = None

    # Local fallback
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[str] = "5432"
    DB_NAME: Optional[str] = None

    # Celery/Redis (hozircha ishlatilmayapti)
    REDIS_URL: str = "redis://redis:6379/0"

    SECRET_KEY: str
    ADMIN_PASSWORD: str

    @property
    def is_prod(self) -> bool:
        return self.ENV.lower() in ("prod", "production")

    @property
    def database_url(self) -> str:
        # Railway bo‘lsa: postgres:// yoki postgresql:// keladi,
        # ikkalasini ham psycopg3 drayveriga o‘tkazamiz.
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            for prefix in ("postgresql+psycopg://", "postgresql://", "postgres://"):
                if url.startswith(prefix):
                    return "postgresql+psycopg://" + url[len(prefix):]
            return url

        # Local bo‘lsa
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
