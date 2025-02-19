"""
Module for user service operations.

This module provides a service class for handling various user-related operations.
"""

from typing import Any

import bcrypt
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.auth.dal import AuthDataAccessLayer
from app.auth.helpers.exceptions import InvalidUserCredentials, UserDoesNotExistError
from app.auth.helpers.messages import AuthMessages
from app.auth.schemas import UserAuthenticateInput, UserRegisterInput
from toolkit.api.enums import HTTPStatusDoc, Status


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

        return {
            "status": Status.SUCCESS,
            "message": AuthMessages.SUCCESS_LOGIN_MESSAGE,
            "data": user,
            "documentationLink": HTTPStatusDoc.HTTP_STATUS_200,
        }

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
