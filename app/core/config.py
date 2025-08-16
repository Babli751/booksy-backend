from pydantic import BaseSettings

class Settings(BaseSettings):
    # API ve güvenlik ayarları
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 hafta

    # Veritabanı URL'si
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

# Ayarları yükle
settings = Settings()
