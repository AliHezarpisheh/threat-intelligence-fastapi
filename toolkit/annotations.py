"""Module contains custom type annotations and utility functions for type hinting."""

from typing import Annotated, Any

JSON = Annotated[dict[str, Any], "This dictionary represents a JSON object"]
