from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_CONNECTION: str
    DB_MIGRATE_PATH: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_WEBHOOK_URL: str
    TELEGRAM_ADMIN_CHAT_ID: int

    BIZON365_X_TOKEN: str
    BIZON365_BC_HOST: str

    class Config:
        env_file = "env/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
