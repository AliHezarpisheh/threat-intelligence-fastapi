"""Contains the TOMLParser class for parsing TOML files."""

import logging
from typing import Any

import tomlkit

from .base import Parser
from .helpers.exceptions import TOMLParseError

logger = logging.getLogger(__name__)


class TOMLParser(Parser):
    """Parses TOML files and loads their content."""

    def read(self) -> Any:
        """
        Read a TOML file and return its content as a dictionary.

        Returns
        -------
        Any
            The parsed content of the TOML file.
        """
        try:
            with self.file_path.open(mode="rb") as file:
                content = tomlkit.load(file)
            return content
        except tomlkit.exceptions.ParseError as err:
            msg = f"Syntax Error in: `{self.file_path}`!"
            logger.error(msg, exc_info=True)
            raise TOMLParseError(msg) from err
