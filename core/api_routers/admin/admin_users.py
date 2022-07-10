from fastapi import APIRouter
from fastapi.params import Depends

from core.api_routers.auth import get_current_user
from core.controllers import ban_user_controller
from core.schemas import BanUserModel
from core.store import UserTable

admin_users_router = APIRouter()


@admin_users_router.delete('/admin/user/ban')
def ban_user(ban_data: BanUserModel, user: UserTable = Depends(get_current_user)):
    ban_user_controller(ban_data, user)
