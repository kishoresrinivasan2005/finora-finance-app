from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Finora Backend"
    debug: bool = True

settings = Settings()
