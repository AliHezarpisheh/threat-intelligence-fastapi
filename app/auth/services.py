"""
Module for user service operations.

This module provides a service class for handling various user-related operations.
"""

from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.auth.dal import AuthDataAccessLayer
from app.auth.helpers.exceptions import (
    InternalTokenError,
    InvalidUserCredentials,
    UserDoesNotExistError,
)
from app.auth.helpers.messages import AuthMessages
from app.auth.models import User
from app.auth.schemas import JwtClaims, UserAuthenticateInput, UserRegisterInput
from config.base import logger, settings
from toolkit.api.enums import HTTPStatusDoc, Status


class TokenService:
    """Service class for token-related operations."""

    TOKEN_TYPE = "Bearer"

    def grant_token(self, user: User) -> dict[str, str]:
        """
        Generate and return a JWT access token for the specified user.

        Parameters
        ----------
        user : User
            The user for whom the token is being generated.

        Returns
        -------
        dict[str, str]
            A dictionary containing the access token and token type.

        Raises
        ------
        TokenError
            If an internal error occurs during token encoding.
        """
        assert settings.jwt_private_key is not None, "JWT private key is not set."
        payload = self._generate_payload(user=user)
        try:
            token = jwt.encode(
                payload=asdict(payload),
                key=settings.jwt_private_key,
                algorithm=settings.jwt_algorithm,
            )
        except TypeError as err:
            logger.error("Couldn't encode the jwt.", exc_info=True)
            raise InternalTokenError(AuthMessages.INTERNAL_TOKEN_ERROR) from err

        return {"access_token": token, "type": self.TOKEN_TYPE}

    def _generate_payload(self, user: User) -> JwtClaims:
        """
        Generate the payload for a JWT token.

        Parameters
        ----------
        user : User
            The user for whom the token payload is being generated.

        Returns
        -------
        JwtClaims
            A dataclass instance representing the JWT claims.
        """
        current_datetime = self._get_current_datetime()
        expiration_datetime = self._add_timedelta(
            dtm=current_datetime, minutes=settings.jwt_lifetime_minutes
        )
        return JwtClaims(
            sub=user.id,
            aud=["all"],
            iat=current_datetime,
            nbf=current_datetime,
            exp=expiration_datetime,
        )

    @staticmethod
    def _get_current_datetime() -> datetime:
        """
        Get the current datetime in UTC.

        Returns
        -------
        datetime
            The current datetime in UTC.
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def _add_timedelta(dtm: datetime, minutes: int) -> datetime:
        """
        Add a timedelta to a given datetime object.

        Parameters
        ----------
        dtm : datetime
            The datetime object to which the timedelta will be added.
        minutes : int
            The number of minutes to add.

        Returns
        -------
        datetime
            A new datetime object with the added timedelta.
        """
        return dtm + timedelta(minutes=minutes)


class AuthService:
    """Service class for user-related operations."""

    def __init__(self, db_session: async_scoped_session[AsyncSession]) -> None:
        """
        Initialize the AuthService.

        Parameters
        ----------
        db_session : async_scoped_session[AsyncSession]
            The database session for asynchronous operations.
        """
        self.db_session = db_session
        self.user_dal = AuthDataAccessLayer(db_session=db_session)
        self.token_service = TokenService()

    async def register(self, user_input: UserRegisterInput) -> dict[str, Any]:
        """
        Register a new user.

        This method hashes the user's password and creates a new user record in the
        database.

        Parameters
        ----------
        user_input : UserRegisterInput
            The user input data required for registration.

        Returns
        -------
        dict[str, Any]
            The newly registered user as the data, plus other metadata related to the
            user registration.
        """
        # Perform password hashing in a separate thread, making event loop responsive
        hashed_password = await run_in_threadpool(
            self.hash_password, user_input.password
        )

        user = await self.user_dal.create_user(
            user_input=user_input, hashed_password=hashed_password
        )
        return {
            "status": Status.CREATED,
            "message": AuthMessages.SUCCESS_REGISTER_MESSAGE,
            "data": user,
            "documentationLink": HTTPStatusDoc.HTTP_STATUS_201,
        }

    async def authenticate(self, user_input: UserAuthenticateInput) -> dict[str, Any]:
        """
        Authenticate a user and initiate OTP (TOTP) setup.

        This method verifies the user's credentials, including email and password,
        and generates an OTP for further authentication steps. If the credentials
        are valid, the OTP is set for the user.

        Parameters
        ----------
        user_input : UserAuthenticateInput
            An object containing the user's login details, including email and password.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the login status, a message, the authenticated
            user's data, and an optional documentation link describing the result of the
            login process.

        Raises
        ------
        InvalidUserCredentials
            If the provided email or password is incorrect.
        """
        try:
            user = await self.user_dal.get_user_by_email(email=user_input.email)
        except UserDoesNotExistError:
            raise InvalidUserCredentials(AuthMessages.INVALID_CREDENTIALS)

        is_password_valid = self.check_password(
            password=user_input.password, hashed_password=user.hashed_password
        )
        if not is_password_valid:
            raise InvalidUserCredentials(AuthMessages.INVALID_CREDENTIALS)

        return self.token_service.grant_token(user=user)

    def hash_password(self, password: str) -> str:
        """
        Hash the user's password.

        This method generates a salt and hashes the password using bcrypt.

        Parameters
        ----------
        password : str
            The plaintext password to be hashed.

        Returns
        -------
        str
            The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            password=password.encode("utf-8"),
            salt=salt,
        )
        return hashed_password.decode("utf-8")

    def check_password(self, password: str, hashed_password: str) -> bool:
        """
        Check if a plaintext password matches a hashed password.

        This method verifies the password by comparing it with its hashed counterpart
        using bcrypt.

        Parameters
        ----------
        password : str
            The plaintext password to verify.
        hashed_password : str
            The hashed password to compare against.

        Returns
        -------
        bool
            True if the password matches the hashed password, otherwise False.
        """
        is_valid = bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )
        return is_valid
