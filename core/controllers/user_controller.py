from core.models import User
from core.schemas import UserUpdateModel, UserAbstractModel, TaskModel, TaskUpdateModel
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


def add_task_controller(user: UserTable, task: TaskModel):
    user = User(user)
    return user.add_task(task)


def get_user_tasks_controller(user: UserTable):
    user = User(user)
    return user.get_my_tasks()


def update_user_tasks_controller(user: UserTable, task_id: int, task_model: TaskUpdateModel):
    user = User(user)
    user.update_my_task_data(task_id, task_model)
