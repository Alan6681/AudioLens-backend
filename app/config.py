from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    YOUTUBE_API_KEY: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  


# Single instance to import across the app
settings = Settings()