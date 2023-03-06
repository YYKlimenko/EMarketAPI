from typing import Any


def get_fields(**fields: Any) -> dict[str, Any]:
    """Delete None fields from the dictionary."""
    return {key: fields[key] for key in fields if fields[key] is not None}
