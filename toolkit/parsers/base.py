"""Defines the abstract base class for parsers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Parser(ABC):
    """Abstract base class for parsers."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize the Parser object.

        Parameters
        ----------
        file_path : str
            The path to the file to be parsed.
        """
        self.file_path = Path(file_path)

    @abstractmethod
    def read(self) -> Any:
        """
        Abstract method to read data.

        This method should be implemented by subclasses to define how data is read.
        """
