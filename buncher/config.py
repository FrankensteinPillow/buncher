from functools import lru_cache
from os import environ

from pydantic import BaseSettings


class Config(BaseSettings):
    db_url: str = environ.get(
        "db_url",
        "sqlite:////home/nortlite/proj/buncher/data.db",
    )
    service_port: int = int(environ.get("service_port", 3520))


@lru_cache
def get_config() -> Config:
    return Config()
