from pydantic import BaseSettings


class Settings(BaseSettings):
    db_name: str = "aits"
    db_user: str = "aitsuser"
    db_password: str = "ehakqoa01!"
    db_host: str = "10.0.3.4"
    db_port: int = 5432

    class Config:
        env_file = ".env"

settings = Settings()
db_config = {
    "dbname": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
    "host": settings.db_host,
    "port": settings.db_port,
}
