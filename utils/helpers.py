import jsonschema


def validate_schema(data: dict, schema: dict):
    """Validates a JSON response against a schema. Raises AssertionError on failure."""
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")


def is_valid_email(email: str) -> bool:
    """Simple email format check."""
    return "@" in email and "." in email.split("@")[-1]