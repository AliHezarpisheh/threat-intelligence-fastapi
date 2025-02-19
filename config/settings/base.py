"""Module for handling all the settings in the application."""

import os
from pathlib import Path
from typing import Annotated, Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .enums import Env
from .openapi import OpenAPISettings


class Settings(BaseSettings):
    """
    Class for handling all the settings in the application.

    Notes
    -----
    The `model_config` attribute is a `SettingsConfigDict` instance. It contains the
    following attributes:
        - toml_file: str
            The file path to the TOML settings file.
        - env_file: str
            The file path to the environments variable settings file.
    """

    # TOML Settings
    openapi: OpenAPISettings

    # .env Settings
    env: Env

    # PostgreSQL settings
    database_url: Annotated[str, Field(..., description="Database connection URL.")]

    # RabbitMQ settings
    amqp_url: Annotated[str, Field(..., description="AMQP-RabbitMQ connection URL.")]

    # Redis settings
    redis_host: Annotated[
        str, Field(..., description="Redis server's hostname/IP.")
    ] = "localhost"
    redis_port: Annotated[
        int, Field(..., description="The port the Redis instance is running.")
    ] = 6037
    redis_db: Annotated[
        int, Field(..., description="Redis database (Accepted values: 0-15)")
    ] = 0
    redis_password: Annotated[str, Field(..., description="Redis instance password.")]
    redis_pool_max_connection: Annotated[
        int, Field(..., description="Redis pool max connection limit.")
    ] = 100

    # API settings
    jwt_algorithm: Annotated[
        str, Field(..., description="The algorithm used for signing the jwt.")
    ]
    jwt_keys_passphrase: Annotated[
        str, Field(..., description="The passphrase for private and public keys.")
    ]
    jwt_private_key_path: Annotated[
        str, Field(..., description="The path to the jwt private key.")
    ]
    jwt_public_key_path: Annotated[
        str, Field(..., description="The path to the jwt public key.")
    ]
    jwt_private_key: Annotated[  # Dynamically loaded.
        RSAPrivateKey | None,
        Field(
            ...,
            description="The jwt private key, loaded from the private key file.",
        ),
    ] = None
    jwt_public_key: Annotated[  # Dynamically loaded.
        RSAPublicKey | None,
        Field(..., description="The jwt public key, loaded from the public key file."),
    ] = None
    jwt_lifetime_minutes: Annotated[
        int, Field(..., description="The jwt lifetime in minutes.")
    ]
    jwt_refresh_token_lifetime_days: Annotated[
        int, Field(..., description="The jwt refresh token lifetime in days.")
    ]
    origins: Annotated[
        list[str], Field(..., description="List of allowed API origins.")
    ]

    @field_validator("jwt_private_key", mode="before")
    @classmethod
    def load_private_key(cls, value: Any, info: ValidationInfo) -> RSAPrivateKey:
        """
        Load and validate the RSA private key for JWT signing.

        This validator checks the existence of the private key file, loads it
        using the passphrase specified in the settings, and ensures that the
        loaded key is an instance of `RSAPrivateKey`.

        Parameters
        ----------
        value : Any
            The original value of the private key field (not used in this validation).
        info : ValidationInfo
            Provides access to the validation context, including settings data.

        Returns
        -------
        RSAPrivateKey
            The RSA private key loaded from the specified path.

        Raises
        ------
        RuntimeError
            If the private key file does not exist or cannot be loaded.
        AssertionError
            If the loaded key is not an instance of `RSAPrivateKey`.
        """
        try:
            private_key_path = info.data["jwt_private_key_path"]
            keys_passphrase = info.data["jwt_keys_passphrase"]
        except KeyError:
            raise RuntimeError(
                "Failed to load the application settings, fix the `.env` file and "
                "check for the `jwt_private_key_path` and `jwt_keys_passphrase` keys."
            )

        path = Path(private_key_path)
        if not path.exists():
            raise RuntimeError(
                "The private and public keys are not generated yet. Try to generate "
                f"keys in the {private_key_path} path, using the command "
                f"`ssh-keygen -t rsa -b 2048 -f {private_key_path}`\n"
                "Make sure that you set the correct passphrase for the files according "
                "to the .env files.\n"
                "You can read `docs/security/create_jwt_keys` for clear instructions."
            )

        with path.open("rb") as key_file:
            private_key = serialization.load_ssh_private_key(
                key_file.read(), password=keys_passphrase.encode("utf-8")
            )
        assert isinstance(private_key, RSAPrivateKey), (
            "jwt_private_key should be instance of `RSAPrivateKey`, but got "
            f"{type(private_key)}"
        )
        return private_key

    @field_validator("jwt_public_key", mode="before")
    @classmethod
    def load_public_key(cls, value: Any, info: ValidationInfo) -> RSAPublicKey:
        """
        Load and validate the RSA public key for JWT verification.

        This validator checks the existence of the public key file, loads it,
        and ensures that the loaded key is an instance of `RSAPublicKey`.

        Parameters
        ----------
        value : Any
            The original value of the public key field (not used in this validation).
        info : ValidationInfo
            Provides access to the validation context, including settings data.

        Returns
        -------
        RSAPublicKey
            The RSA public key loaded from the specified path.

        Raises
        ------
        RuntimeError
            If the public key file does not exist or cannot be loaded.
        AssertionError
            If the loaded key is not an instance of `RSAPublicKey`.
        """
        try:
            public_key_path = info.data["jwt_public_key_path"]
        except KeyError:
            raise RuntimeError(
                "Failed to load the application settings, fix the `.env` file and "
                "check for the `jwt_public_key_path` key."
            )

        path = Path(public_key_path)
        if not path.exists():
            raise RuntimeError(
                "The private and public keys are not generated yet. Try to generate "
                f"keys in the {public_key_path} path, using the command "
                f"`ssh-keygen -t rsa -b 2048 -f {public_key_path}`\n"
                "Make sure that you set the correct passphrase for the files according "
                "to the .env files.\n"
                "You can read `docs/security/create_jwt_keys` for clear instructions."
            )

        with path.open("rb") as key_file:
            public_key = serialization.load_ssh_public_identity(key_file.read())
        assert isinstance(public_key, RSAPublicKey), (
            "jwt_private_key should be instance of `RSAPublicKey`, but got "
            f"{type(public_key)}"
        )
        return public_key

    # Settings config
    model_config = SettingsConfigDict(
        toml_file="settings.toml",
        env_file=f".env.{os.getenv('ENV', 'development')}",
        case_sensitive=False,
        use_enum_values=True,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customise the settings sources."""
        return (
            init_settings,  # Initial settings
            TomlConfigSettingsSource(settings_cls),  # Read from .toml file
            DotEnvSettingsSource(settings_cls),  # Read from .env file
            env_settings,  # Read from environments variables
            file_secret_settings,  # Read from any file secret settings if applicable
        )
