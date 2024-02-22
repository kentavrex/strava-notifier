from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    TG_TOKEN: str
    AUTH_TOKEN: str


config = Config()
