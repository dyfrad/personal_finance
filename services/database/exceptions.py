"""Custom database exceptions and error handling."""

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Exception for database connection issues."""
    pass


class DatabaseQueryError(DatabaseError):
    """Exception for database query issues."""
    pass 