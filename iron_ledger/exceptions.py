class IronLedgerError(Exception):
    """Base exception for all Iron Ledger errors."""
    pass

class ApiError(IronLedgerError):
    """Raised when an API request fails."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ValidationError(IronLedgerError):
    """Raised when data validation fails."""
    pass

class MappingError(IronLedgerError):
    """Raised when exercise mapping fails."""
    pass

class ConfigError(IronLedgerError):
    """Raised when configuration is invalid or missing."""
    pass
