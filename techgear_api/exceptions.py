class DatabaseError(RuntimeError):
    """Base class for database configuration and connection failures."""
    pass


class DatabaseConfigurationError(DatabaseError):
    """MongoDB settings are missing or invalid."""
    pass


class DatabaseConnectionError(DatabaseError):
    """The application could not connect to MongoDB."""
    pass
