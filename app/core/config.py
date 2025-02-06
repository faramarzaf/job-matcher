from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str
    MONGO_USER: str
    MONGO_PASSWORD: str

    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "allow"

    @property
    def mongodb_uri(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@mongo:27017/?authSource=admin"


settings = Settings()
