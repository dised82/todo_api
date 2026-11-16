from http import HTTPStatus

# here lies all the errors of the application


class AppError(Exception):
    """Base class: every error of the app inherits from it."""

    status = HTTPStatus.INTERNAL_SERVER_ERROR


class NotFound(AppError):
    """The list / element / user does not exist (or isn't yours)."""

    status = HTTPStatus.NOT_FOUND  # 404


class AlreadyExists(AppError):
    """Unique value already taken (ex: username)."""

    status = HTTPStatus.CONFLICT  # 409


class InvalidData(AppError):
    """Bad input: empty name, username too long..."""

    status = HTTPStatus.BAD_REQUEST  # 400


class Unauthorized(AppError):
    """Wrong username or password / not logged in."""

    status = HTTPStatus.UNAUTHORIZED  # 401
