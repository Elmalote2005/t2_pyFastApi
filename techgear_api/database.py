from pathlib import Path
from threading import Lock

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError
from pymongo.database import Database

if __package__:
    from .exceptions import DatabaseConfigurationError, DatabaseConnectionError
else:
    from exceptions import DatabaseConfigurationError, DatabaseConnectionError


class Settings(BaseSettings):
    mongo_uri: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MONGO_URI", "MONGODB_URI"),
    )
    mongo_database: str = Field(
        default="techgear_db",
        validation_alias=AliasChoices("MONGO_DATABASE", "MONGODB_DATABASE"),
    )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).with_name(".env"),
        env_file_encoding="utf-8-sig",
        extra="ignore",
    )


settings = Settings()
_client: MongoClient | None = None
_client_lock = Lock()


def get_database() -> Database:
    global _client

    uri = settings.mongo_uri
    if not uri or not uri.strip():
        raise DatabaseConfigurationError(
            "MongoDB no está configurado. Define MONGO_URI o MONGODB_URI."
        )

    if _client is None:
        with _client_lock:
            if _client is None:
                client = None
                try:
                    client = MongoClient(
                        uri.strip(), serverSelectionTimeoutMS=5000
                    )
                    client.admin.command("ping")
                except ConfigurationError as exc:
                    if client is not None:
                        client.close()
                    raise DatabaseConfigurationError(
                        "La URI configurada para MongoDB no es válida."
                    ) from exc
                except PyMongoError as exc:
                    if client is not None:
                        client.close()
                    raise DatabaseConnectionError(
                        "No fue posible conectar con MongoDB."
                    ) from exc
                _client = client

    return _client[settings.mongo_database]


def close_database() -> None:
    global _client

    with _client_lock:
        if _client is not None:
            _client.close()
            _client = None
