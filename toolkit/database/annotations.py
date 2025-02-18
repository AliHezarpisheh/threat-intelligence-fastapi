"""Module defining annotated types for database configurations."""

from typing import Annotated

str64 = Annotated[str, 64]
str255 = Annotated[str, 255]

text = Annotated[str, "Text"]
