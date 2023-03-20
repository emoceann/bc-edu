from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    NOTION_AUTH_TOKEN: str
    NOTION_PAGE_IDS: str
    NOTION_PATH_TO_FILE: str

    class Config:
        env_file = "env/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
