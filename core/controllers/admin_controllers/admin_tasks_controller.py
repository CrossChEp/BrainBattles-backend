"""This module contains controllers that regard to admin tasks functional

Functions:
    hide_task_controller
        hides task from open access
    add_task_to_public_controller
        adds task to open access
"""


from core.exceptions import throw_exception_if_user_have_no_rights
from core.models import User
from core.store import UserTable


def hide_task_controller(task_id: int, user: UserTable):
    """Controller that provides ``User`` state pattern functional by hiding the task
    using it's id

    :param task_id: int
        (Id of task that should be hidden)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Helper`` , it'll throw the exception )
    """
    user = User(user)
    throw_exception_if_user_have_no_rights(user.hide_task, task_id)


def add_task_to_public_controller(task_id: int, user: UserTable):
    """Controller that provides ``User`` state pattern functional by adding the task to open access.

    :param task_id: int
        (Id of task that should added to open access)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Helper`` , it'll throw the exception )
    """
    user = User(user)
    throw_exception_if_user_have_no_rights(user.add_task_to_public, task_id)
