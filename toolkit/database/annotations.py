"""Module defining annotated types for database configurations."""

from typing import Annotated

str63 = Annotated[str, 63]
str255 = Annotated[str, 255]

text = Annotated[str, "Text"]
