class GoveeError(Exception):
    """Base exception for Govee-related errors."""
    pass

class GoveeAPIError(GoveeError):
    """Raised when API communication fails."""
    pass

class GoveeConfigError(GoveeError):
    """Raised when there are configuration-related errors."""
    pass

class GoveeValidationError(GoveeError):
    """Raised when input validation fails."""
    pass

class GoveeConnectionError(GoveeError):
    """Raised when network connection issues occur."""
    pass

class GoveeTimeoutError(GoveeError):
    """Raised when requests timeout."""
    pass