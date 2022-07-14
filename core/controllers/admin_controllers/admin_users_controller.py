"""This module contains controllers that regard to admin users functional

Functions:
    ban_user_controller
        bans user
    edit_user_controller
        edits all user information
    delete_user_controller
        deletes user
    promote_user_to_default_controller
        promotes user to ``default`` state
    promote_user_to_helper_controller
        promotes user to ``helper`` state
    promote_user_to_moderator_controller
        promotes user to ``moderator`` state
    promote_user_to_admin_controller
        promotes user to ``admin`` state
    promote_user_to_elder_admin_controller
        promotes user to ``elder_admin`` state
    promote_user_to_ceo_controller
        promotes user to ``ceo`` state
"""


from sqlalchemy.orm import Session

from core.exceptions import throw_exception_if_user_have_no_rights
from core.middlewares.database_session import generate_session
from core.models import User, get_user_by_id, promote_user
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable


def ban_user_controller(ban_data: BanUserModel, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    banning user permanently or temporary. This method available after ``Moderator`` state,
    but moderators can only ban temporary. After ``Admin`` state, users can ban permanently

    :param ban_data: BanUserModel
        (Model of ban data that contains user id and term of ban)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Moderator`` ,
        it'll throw the exception )
    """
    user = User(user)
    throw_exception_if_user_have_no_rights(user.ban_user, ban_data)


def edit_user_controller(user_id: int, new_user_data: UserUpdateAdminModel,
                         user: UserTable):
    """Controller that provides ``User`` state pattern functional by
    editing every information of user. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, whose data should be updated)
    :param new_user_data: UserUpdateAdminModel
        (Update model that contains all the user fields)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception)
    """
    user = User(user)
    throw_exception_if_user_have_no_rights(user.edit_another_user, user_id, new_user_data)


def delete_another_user_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    deletion user. This method available after ``ElderAdmin`` state

    :param user_id: int
        (Id of user, that should be deleted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Elder Admin`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    user_we_want_to_delete = get_user_by_id(user_id, session)
    throw_exception_if_user_have_no_rights(user.delete_another_user, user_we_want_to_delete)


def promote_user_to_default_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    promotion user to default state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    promote_user(user.promote_to_default, user_id, session)


def promote_user_to_helper_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    promotion user to helper state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    promote_user(user.promote_to_helper, user_id, session)


def promote_user_to_moderator_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    promotion user to moderator state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    promote_user(user.promote_to_moderator, user_id, session)


def promote_user_to_admin_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    promotion user to admin state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    promote_user(user.promote_to_admin, user_id, session)


def promote_user_to_elder_admin_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    promotion user to elder admin state. This method available after ``Elder Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Elder Admin`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    promote_user(user.promote_to_elder_admin, user_id, session)


def promote_user_to_ceo_controller(user_id: int, user: UserTable) -> None:
    """Controller that provides ``User`` state pattern functional by
    promotion user to ceo state. This method available after ``Ceo`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Ceo`` ,
        it'll throw the exception )
    """
    user = User(user)
    session: Session = next(generate_session())
    promote_user(user.promote_to_ceo, user_id, session)
