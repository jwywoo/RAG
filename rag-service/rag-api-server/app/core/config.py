from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    # comment it when you test it in local
    # OPENAI_API_KEY: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
