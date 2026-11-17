from pathlib import Path
from threading import Lock
import logging

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError
from pymongo.database import Database

if __package__:
    from .exceptions import DatabaseConfigurationError, DatabaseConnectionError
else:
    from exceptions import DatabaseConfigurationError, DatabaseConnectionError

logger = logging.getLogger(__name__)


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
        # ⚠️ ELIMINAMOS env_file — Render usa variables de entorno del sistema
        extra="ignore",
    )


settings = Settings()
_client: MongoClient | None = None
_db: Database | None = None
_client_lock = Lock()


def get_database() -> Database:
    global _client, _db

    uri = settings.mongo_uri
    if not uri or not uri.strip():
        logger.error("❌ MONGO_URI no está configurada")
        raise DatabaseConfigurationError(
            "MongoDB no está configurado. Define MONGO_URI como variable de entorno."
        )

    # Devolvemos la base de datos en caché si ya existe
    if _db is not None:
        return _db

    with _client_lock:
        if _db is not None:
            return _db
        
        client = None
        try:
            client = MongoClient(
                uri.strip(),
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                connectTimeoutMS=10000,
            )
            # Verificar conexión
            client.admin.command("ping")
            logger.info("✅ Conectado exitosamente a MongoDB")
            
            _db = client[settings.mongo_database]
            _client = client
            return _db
            
        except ConfigurationError as exc:
            if client is not None:
                client.close()
            logger.error(f"❌ URI de MongoDB inválida: {exc}")
            raise DatabaseConfigurationError(
                "La URI configurada para MongoDB no es válida."
            ) from exc
            
        except PyMongoError as exc:
            if client is not None:
                client.close()
            logger.error(f"❌ No se pudo conectar a MongoDB: {exc}")
            raise DatabaseConnectionError(
                "No fue posible conectar con MongoDB. Revisa la URI y el acceso de IP."
            ) from exc


def close_database() -> None:
    global _client, _db

    with _client_lock:
        if _client is not None:
            _client.close()
            _client = None
            _db = None
            logger.info("🔌 Conexión a MongoDB cerrada")
