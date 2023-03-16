from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_CONNECTION: str
    DB_MIGRATE_PATH: str

    TELEGRAM_BOT_LINK: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_USERNAME: str
    TELEGRAM_WEBHOOK_URL: str
    TELEGRAM_ADMIN_CHAT_ID: int
    TELEGRAM_BOT_STATE_PATH: str

    BIZON365_X_TOKEN: str
    BIZON365_BC_HOST: str
    BIZON365_API_HOST: str

    NOWPAYMENT_TOKEN: str
    NOWPAYMENT_CALLBACK_AUTH_TOKEN: str
    NOWPAYMENT_URL: str

    GOOGLE_SHEET_URL_TOKEN: str

    class Config:
        env_file = "env/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
