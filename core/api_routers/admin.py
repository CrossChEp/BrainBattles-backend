from fastapi import APIRouter
from fastapi.params import Depends

from core.api_routers.auth import get_current_user
from core.controllers import hide_task_controller, add_task_to_public_controller
from core.store import UserTable

admin_router = APIRouter()


@admin_router.delete('/admin/task/hide/{task_id}')
def hide_task(task_id: int, user: UserTable = Depends(get_current_user)):
    hide_task_controller(task_id, user)


@admin_router.post('/admin/task/post/{task_id}')
def add_task_to_public(task_id: int, user: UserTable = Depends(get_current_user)):
    add_task_to_public_controller(task_id, user)
