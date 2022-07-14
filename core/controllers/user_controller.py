from core.exceptions import throw_exception_if_user_have_no_rights
from core.models import User
from core.schemas import UserUpdateModel, UserAbstractModel, TaskAddModel, TaskUpdateModel
from core.store import UserTable


def get_all_users_controller(user: UserTable):
    user = User(user)
    return user.get_users()


def delete_user_controller(user: UserTable):
    user = User(user)
    user.delete()


def update_user_data_controller(user: UserTable, new_user_data: UserUpdateModel):
    user = User(user)
    user.update(new_user_data)


def get_user_by_id_controller(user: UserTable, user_id: int):
    user = User(user)
    return user.get_user(UserAbstractModel(id=user_id))


def add_task_controller(user: UserTable, task: TaskAddModel):
    user = User(user)
    return user.add_task(task)


def get_user_tasks_controller(user: UserTable):
    user = User(user)
    return user.get_my_tasks()


def update_user_tasks_controller(user: UserTable, task_id: int, task_model: TaskUpdateModel):
    user = User(user)
    user.update_my_task_data(task_id, task_model)


def delete_user_task_controller(user: UserTable, task_id: int):
    user = User(user)
    user.delete_my_task(task_id)


def get_task_by_id_controller(user: UserTable, task_id: int):
    user = User(user)
    return user.get_task_using_id(task_id)
