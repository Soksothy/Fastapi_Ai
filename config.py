from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434/api/generate"
    model_name: str = "llama3.2"

settings = Settings()
