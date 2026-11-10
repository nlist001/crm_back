from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Описываем переменные и их типы
    #DB_URL: str = 'sqlite:///./todo/todo.db'
    DB_URL: str = 'postgresql://postgres:1@localhost/crmpy'
    DEBUG: bool = False  # значение по умолчанию
    SECRET_KEY: str = "2f7nst589ikjgdd456789086543484f5g2w35r56h9iu8776541s0kbcdg"
    ALGORITHM: str = "HS256"
    # Указываем Pydantic читать данные из .env файла
    model_config = SettingsConfigDict(env_file=".env")

# Создаем синглтон настроек
settings = Settings()

