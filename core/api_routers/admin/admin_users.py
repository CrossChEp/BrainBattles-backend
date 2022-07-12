from fastapi import APIRouter
from fastapi.params import Depends

from core.api_routers.auth import get_current_user
from core.controllers import ban_user_controller, edit_user_controller, delete_another_user_controller
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable

admin_users_router = APIRouter()


@admin_users_router.delete('/admin/user/ban')
def ban_user(ban_data: BanUserModel, user: UserTable = Depends(get_current_user)):
    ban_user_controller(ban_data, user)


@admin_users_router.put('/admin/user/edit/{user_id}')
def edit_user(user_id: int, user_update_model: UserUpdateAdminModel,
              user: UserTable = Depends(get_current_user)) -> None:
    edit_user_controller(user_id, user_update_model, user)


@admin_users_router.delete('/admin/user/delete/{user_id}')
def delete_user(user_id: int, user: UserTable = Depends(get_current_user)) -> None:
    delete_another_user_controller(user_id, user)
