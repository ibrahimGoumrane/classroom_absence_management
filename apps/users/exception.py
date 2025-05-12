from rest_framework.views import exception_handler

def flatten_errors(errors, parent_key=""):
    """
    Recursively flattens nested errors into a single dictionary.
    Example:
        Input: {"user": {"email": ["This email is already registered."]}}
        Output: {"email": "This email is already registered."}
    """
    flattened = {}

    for key, value in errors.items():
        new_key = key

        if isinstance(value, dict):
            flattened.update(flatten_errors(value, new_key))  # Recursively flatten
        elif isinstance(value, list) and len(value) > 0:
            flattened[new_key] = value[0]  # Keep only the first error message per field
        else:
            flattened[new_key] = value  # Handle non-list errors

    return flattened


def custom_exception_handler(exc, context):
    """
    Custom error response format:
    {
        "error": "This email is already registered."
    }
    """
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        flattened_errors = flatten_errors(response.data)
        if flattened_errors:
            # Get the first error message only
            first_error = next(iter(flattened_errors.values()))
            response.data = {"error": first_error}

    return response