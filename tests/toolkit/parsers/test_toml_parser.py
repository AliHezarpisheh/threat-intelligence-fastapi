"""Unit tests for the TOMLParser class."""

from unittest.mock import mock_open, patch

import pytest

from toolkit.parsers import TOMLParser
from toolkit.parsers.helpers.exceptions import TOMLParseError

SAMPLE_TOML_CONTENT = """
[info]
name = "John"
age = 30
"""

FILE_PATH = "test.toml"


@pytest.fixture
def toml_parser() -> TOMLParser:
    """Fixture to instantiate TOMLParser."""
    return TOMLParser(file_path=FILE_PATH)


@pytest.mark.smoke
def test_read(toml_parser: TOMLParser) -> None:
    """Test reading a valid TOML file."""
    with patch("pathlib.Path.open", mock_open(read_data=SAMPLE_TOML_CONTENT)):
        content = toml_parser.read()

    assert content == {"info": {"name": "John", "age": 30}}


def test_read_invalid_syntax_toml_file(
    toml_parser: TOMLParser,
) -> None:
    """Test reading an invalid TOML file."""
    with patch("pathlib.Path.open", mock_open(read_data="invalid syntax")):
        with pytest.raises(TOMLParseError, match="Syntax Error in: `test.toml`!"):
            toml_parser.read()
