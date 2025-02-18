"""Module provides ORM functionality for database interaction."""

from typing import ClassVar

from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase

from .annotations import str64, str255, text


class Base(DeclarativeBase):
    """Base class for declarative ORM models."""

    type_annotation_map: ClassVar = {
        str64: String(64),
        str255: String(255),
        text: Text,
    }
