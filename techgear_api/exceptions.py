class DatabaseError(RuntimeError):
    """Base class for database configuration and connection failures."""


class DatabaseConfigurationError(DatabaseError):
    """MongoDB settings are missing or invalid."""


class DatabaseConnectionError(DatabaseError):
    """The application could not connect to MongoDB."""
