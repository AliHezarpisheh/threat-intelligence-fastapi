"""
Module containing repository data access layer for auth related operations.

This module provides methods for interacting with the database to perform
CRUD operations on the user model.
"""

from __future__ import annotations

from typing import NoReturn

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.auth.helpers.exceptions import (
    DuplicateUserError,
    UserDoesNotExistError,
)
from app.auth.models import User
from app.auth.schemas import UserRegisterInput
from config.base import logger


class AuthDataAccessLayer:
    """Data access layer for auth related operations."""

    def __init__(self, db_session: async_scoped_session[AsyncSession]) -> None:
        """
        Initialize the AuthDataAccessLayer.

        Parameters
        ----------
        db_session : async_scoped_session[AsyncSession]
            The database session for asynchronous operations.
        """
        self.db_session = db_session

    async def create_user(
        self, user_input: UserRegisterInput, hashed_password: str
    ) -> User:
        """
        Create a new user.

        Parameters
        ----------
        user_input : UserRegisterInput
            User data to create a new user.
        hashed_password : str
            Hashed password for the new user.

        Returns
        -------
        User
            The newly created user.
        """
        stmt = (
            insert(User)
            .values(
                username=user_input.username,
                email=user_input.email,
                hashed_password=hashed_password,
                is_active=True,
            )
            .returning(User)
        )

        async with self.db_session.begin():
            try:
                result = await self.db_session.execute(stmt)
                user = result.scalar_one()
                return user
            except IntegrityError as exc:
                await self.db_session.rollback()
                self.handle_integrity_error(exc=exc)

    @staticmethod
    def handle_integrity_error(exc: IntegrityError) -> NoReturn:
        """
        Handle integrity error.

        Raises
        ------
        DuplicateUserError
            If the error is due to a duplicate username or email.
        """
        if "duplicate key value violates unique constraint" in str(exc):
            if "auth__user_username_key" in str(exc):
                raise DuplicateUserError(
                    "User with this username already exists"
                ) from exc
            elif "auth__user_email_key" in str(exc):
                raise DuplicateUserError("User with this email already exists") from exc
        logger.warning("Unhandled Integrity error occurred. The error: %s", exc)
        raise exc

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email address.

        This method queries the database for a user with the given email address.
        If no user is found, it handles the `NoResultFound` exception.

        Parameters
        ----------
        email : str
            The email address of the user to be retrieved.

        Returns
        -------
        User
            The user object associated with the given email.

        Raises
        ------
        UserDoesNotExistError
            If no user with the specified email exists in the database.
        """
        stmt = select(User).where(
            User.email == email,
            User.is_active == True,  # noqa: E712
        )

        try:
            async with self.db_session.begin():
                result = await self.db_session.execute(stmt)
                user = result.scalar_one()
            return user
        except NoResultFound as err:
            self.handle_no_result_found_error(err)

    @staticmethod
    def handle_no_result_found_error(exc: NoResultFound) -> NoReturn:
        """
        Handle no result found error.

        Raises
        ------
        NoResultFound
            If the user is not found.
        """
        raise UserDoesNotExistError("User does not exists.")
