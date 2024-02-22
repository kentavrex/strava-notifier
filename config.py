from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    TG_TOKEN: str
    KEYCLOACK_REFRESH_TOKEN: str
    KEYCLOACK_CLIENT_ID: str


config = Config()
