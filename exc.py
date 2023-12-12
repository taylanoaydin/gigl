class DatabaseError(Exception):
    """Exception raised for errors related to the database operations."""
    pass

class ServerError(Exception):
    """Exception raised for errors related to the server operations."""
    pass

class AuthenticationError(Exception):
    """Exception raised for errors during authentication."""
    pass

class EmailSendingError(Exception):
    """Exception raised for errors during email sending."""
    pass