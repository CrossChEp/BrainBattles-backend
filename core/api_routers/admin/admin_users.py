"""This module contains api routers that regard to admin users functional

Functions:
    ban_user
        bans user
    edit_user
        edits all user information
    delete_user
        deletes user
    promote_user_to_default
        promotes user to ``default`` state
    promote_user_to_helper
        promotes user to ``helper`` state
    promote_user_to_moderator
        promotes user to ``moderator`` state
    promote_user_to_admin
        promotes user to ``admin`` state
    promote_user_to_elder_admin
        promotes user to ``elder_admin`` state
    promote_user_to_ceo
        promotes user to ``ceo`` state
"""


from fastapi import APIRouter
from fastapi.params import Depends

from core.api_routers.auth import get_current_user
from core.controllers import ban_user_controller, edit_user_controller, delete_another_user_controller, \
    promote_user_to_helper_controller, promote_user_to_default_controller, promote_user_to_admin_controller, \
    promote_user_to_elder_admin_controller, promote_user_to_moderator_controller, promote_user_to_ceo_controller
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable

admin_users_router = APIRouter()


@admin_users_router.delete('/admin/user/ban')
def ban_user(ban_data: BanUserModel, user: UserTable = Depends(get_current_user)):
    """DELETE /admin/user/ban

    Bans user permanently or temporary. This method available after ``Moderator`` state,
    but moderators can only ban temporary. After ``Admin`` state, users can ban permanently

    :param ban_data: BanUserModel
        (Model of ban data that contains user id and term of ban)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Moderator`` ,
        it'll throw the exception )
    """
    ban_user_controller(ban_data, user)


@admin_users_router.put('/admin/user/edit/{user_id}')
def edit_user(user_id: int, user_update_model: UserUpdateAdminModel,
              user: UserTable = Depends(get_current_user)) -> None:
    """PUT /admin/user/edit/{user_id}

    Edits every information of user. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, whose data should be updated)
    :param user_update_model: UserUpdateAdminModel
        (Update model that contains all the user fields)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    edit_user_controller(user_id, user_update_model, user)


@admin_users_router.delete('/admin/user/delete/{user_id}')
def delete_user(user_id: int, user: UserTable = Depends(get_current_user)) -> None:
    """DELETE /admin/user/delete/{user_id}

    Deletes user. This method available after ``ElderAdmin`` state

    :param user_id: int
        (Id of user, that should be deleted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Elder Admin`` ,
        it'll throw the exception )
    """
    delete_another_user_controller(user_id, user)


@admin_users_router.post('/admin/user/promote/default/{user_id}')
def promote_user_to_default(user_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/user/promote/default/{user_id}

    Promotes user to default state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    promote_user_to_default_controller(user_id, user)


@admin_users_router.post('/admin/user/promote/helper/{user_id}')
def promote_user_to_helper(user_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/user/promote/helper/{user_id}

    Promotes user to helper state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    promote_user_to_helper_controller(user_id, user)


@admin_users_router.post('/admin/user/promote/moderator/{user_id}')
def promote_user_to_moderator(user_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/user/promote/moderator/{user_id}

    Promotes user to default moderator. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    promote_user_to_moderator_controller(user_id, user)


@admin_users_router.post('/admin/user/promote/admin/{user_id}')
def promote_user_to_admin(user_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/user/promote/admin/{user_id}

    Promotes user to admin state. This method available after ``Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Admin`` ,
        it'll throw the exception )
    """
    promote_user_to_admin_controller(user_id, user)


@admin_users_router.post('/admin/user/promote/elder_admin/{user_id}')
def promote_user_to_elder_admin(user_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/user/promote/elder_admin/{user_id}

    Promotes user to default state. This method available after ``Elder Admin`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Elder Admin`` ,
        it'll throw the exception )
    """
    promote_user_to_elder_admin_controller(user_id, user)


@admin_users_router.post('/admin/user/promote/ceo/{user_id}')
def promote_user_to_ceo(user_id: int, user: UserTable = Depends(get_current_user)):
    """POST /admin/user/promote/ceo/{user_id}

    Promotes user to default state. This method available after ``Ceo`` state

    :param user_id: int
        (Id of user, that should be promoted)
    :param user: UserTable
        (User that currently logged in. If user's state less than ``Ceo`` ,
        it'll throw the exception )
    """
    promote_user_to_ceo_controller(user_id, user)
