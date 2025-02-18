"""Module containing custom exceptions used by the parsing toolkit."""


class TOMLParseError(Exception):
    """Raise when an error occurs while parsing TOML data."""

    pass


class ExcelParseError(Exception):
    """Raise when an error occurs while parsing Excel data."""

    pass
