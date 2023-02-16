from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_CONNECTION: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_WEBHOOK_URL: str

    class Config:
        env_file = "env/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
