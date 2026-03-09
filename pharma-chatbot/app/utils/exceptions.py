STORE_NOT_FOUND = "store_not_found"
BRAND_NOT_FOUND = "brand_not_found"
AMBIGUOUS_BRAND = "ambiguous_brand"
INVALID_INTENT = "invalid_intent"
INVALID_PARAMETERS = "invalid_parameters"
BACKEND_ERROR = "backend_error"

class InvalidIntentException(Exception):
    """Raised when intent validation fails or access is denied."""
    pass