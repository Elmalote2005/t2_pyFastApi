from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, Mock, patch

from fastapi.testclient import TestClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

from techgear_api import database
from techgear_api.exceptions import (
    DatabaseConfigurationError,
    DatabaseConnectionError,
)
from techgear_api import main


class DatabaseTests(unittest.TestCase):
    def test_accepts_both_supported_uri_environment_names(self):
        current_uri = "mongodb://localhost:27017"

        with_uri = database.Settings(_env_file=None, MONGO_URI=current_uri)
        with_legacy_uri = database.Settings(
            _env_file=None, MONGODB_URI=current_uri
        )

        self.assertEqual(with_uri.mongo_uri, current_uri)
        self.assertEqual(with_legacy_uri.mongo_uri, current_uri)

    def test_reads_uri_from_utf8_env_file_with_bom(self):
        with TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text(
                "MONGO_URI=mongodb://localhost:27017\n",
                encoding="utf-8-sig",
            )

            settings = database.Settings(_env_file=env_file)

        self.assertEqual(settings.mongo_uri, "mongodb://localhost:27017")

    def test_missing_uri_raises_configuration_error_without_connecting(self):
        with (
            patch.object(database.settings, "mongo_uri", None),
            patch.object(database, "_client", None),
            patch.object(database, "MongoClient") as mongo_client,
        ):
            with self.assertRaises(DatabaseConfigurationError):
                database.get_database()

        mongo_client.assert_not_called()

    def test_connection_failure_is_reported_as_database_exception(self):
        client = Mock()
        client.admin.command.side_effect = ServerSelectionTimeoutError(
            "unavailable"
        )

        with (
            patch.object(database.settings, "mongo_uri", "mongodb://db"),
            patch.object(database, "_client", None),
            patch.object(database, "MongoClient", return_value=client),
        ):
            with self.assertRaises(DatabaseConnectionError):
                database.get_database()

        client.close.assert_called_once()

    def test_successful_connection_is_cached(self):
        client = MagicMock()

        with (
            patch.object(database.settings, "mongo_uri", "mongodb://db"),
            patch.object(database, "_client", None),
            patch.object(
                database, "MongoClient", return_value=client
            ) as factory,
        ):
            first_database = database.get_database()
            second_database = database.get_database()

        self.assertIs(first_database, client.__getitem__.return_value)
        self.assertIs(second_database, first_database)
        factory.assert_called_once_with(
            "mongodb://db", serverSelectionTimeoutMS=5000
        )
        client.admin.command.assert_called_once_with("ping")

    def test_invalid_uri_is_reported_as_configuration_exception(self):
        with (
            patch.object(database.settings, "mongo_uri", "not-a-uri"),
            patch.object(database, "_client", None),
            patch.object(
                database,
                "MongoClient",
                side_effect=ConfigurationError("invalid URI"),
            ),
        ):
            with self.assertRaises(DatabaseConfigurationError):
                database.get_database()

    def test_api_returns_service_unavailable_when_database_is_unconfigured(self):
        with (
            patch.object(database.settings, "mongo_uri", None),
            patch.object(main, "_admin_initialized", False),
        ):
            response = TestClient(main.app).get("/productos")

        self.assertEqual(response.status_code, 503)
        self.assertIn("MONGO_URI", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
