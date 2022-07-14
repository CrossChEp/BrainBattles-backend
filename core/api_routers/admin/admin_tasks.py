"""This module contains api routers that regard to admin tasks functional

Functions:
    hide_task
        hides task from open access
    add_task_to_public
        adds task to open access
"""


from fastapi import APIRouter
from fastapi.params import Depends

from core.api_routers.auth import get_current_user
from core.controllers import hide_task_controller, add_task_to_public_controller
from core.store import UserTable

admin_task_router = APIRouter()


@admin_task_router.delete('/admin/task/hide/{task_id}')
def hide_task(task_id: int, user: UserTable = Depends(get_current_user)):
    """``DELETE /admin/task/hide/{task_id}``

    Hides task from open access. This method available after ``Helper`` state.

    :param task_id: int
        (Id of task that should be hidden)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Helper`` , it'll throw the exception )
    """
    hide_task_controller(task_id, user)


@admin_task_router.post('/admin/task/post/{task_id}')
def add_task_to_public(task_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/task/post/{task_id}

    Adds task to open access. This method available after ``Helper`` state.

    :param task_id: int
        (Id of task that should added to open access)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Helper`` , it'll throw the exception )
    """
    add_task_to_public_controller(task_id, user)
