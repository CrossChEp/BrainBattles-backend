"""
This module contains User state patter, that allows to make all the actions
with users

Classes:
    User
    UserState
    DefaultState
    HelperState
    ModeratorState
    AdminState
    ElderAdminState
    CeoState
    BannedState

    Functions:
        convert_string_state_to_class
            converts state string format to class

"""
from typing import List

from sqlalchemy.orm import Session

from core.configs import DEFAULT, HELPER, MODERATOR, ADMIN, ELDER_ADMIN, CEO
from core.configs.config import HIDDEN, OPEN
from core.middlewares.database_session import generate_session
from core.models import task_add, user_tasks_get, update_task_data, get_task_by_id, get_concrete_task_with_every_state
from core.models.admin.users.admin_users_methods import ban_user_temporary, ban_user_permanently, edit_user, \
    promote_user_to_another_state
from core.models.tasks.tasks_methods import delete_user_task
from core.models.user.user_methods import update_user_data, delete_user_from_database, get_user_by_id, get_user, users_get
from core.schemas import UserAbstractModel, UserUpdateModel, TaskAddModel, TaskUpdateModel, BanUserModel, \
    UserUpdateAdminModel, UserGetModel, TaskGetModel
from core.store import UserTable


class User:
    """ Class that contains all user methods
        fields:
        __user: UserTable
            user's database object
        __state: UserState
            user's state in class format
    """

    def __init__(self, user: UserTable):
        self.__user: UserTable = user
        self.__state: UserState = convert_string_state_to_class(
            state=user.state,
            user=self,
            user_database=self.__user
        )

    def delete(self) -> None:
        """deletes this user
        :return: None
        """
        self.__state.delete()

    def update(self, user_update_data: UserUpdateModel) -> None:
        """updates this user data

        :return: None
        """
        self.__state.update(user_update_data)

    def get_users(self) -> List[UserGetModel]:
        """gets all users from database

        :return: List[UserGetModel]
        """
        return self.__state.get_users()

    def get_user(self, user: UserAbstractModel) -> UserGetModel:
        """gets concrete user

        :param user: UserAbstractModel
            (Model fields for which the search will be performed)
        :return: UserGetModel
        """
        return self.__state.get_concrete_user(user)

    def add_task(self, task: TaskAddModel) -> None:
        """adds task to database

        :param task: TaskAddModel
            (Model that contains fields that will have future task)
        :return None
        """
        self.__state.add_task(task)

    def get_my_tasks(self) -> List[TaskGetModel]:
        """gets all user's tasks

        :return: List[TaskGetModel]
        """
        return self.__state.get_my_tasks()

    def update_my_task_data(self, task_id: int, task_model: TaskUpdateModel) -> None:
        """updates user's task

        :param task_id: int
            (id of task that will be updated)
        :param task_model: TaskUpdateModel
            (Model that contains new task data)
        :return: None
        """
        self.__state.update_my_task_data(task_id, task_model)

    def delete_my_task(self, task_id: int) -> None:
        """deletes user's task

        :param task_id: int
            (id of task that will be deleted)
        :return: None
        """
        self.__state.delete_my_task(task_id)

    def get_task_using_id(self, task_id: int) -> TaskGetModel:
        """gets task using id

        :param task_id: int
            (id of task that will be returned)
        :return: TaskGetModel
        """
        return self.__state.get_task_using_id(task_id)

    def add_task_to_public(self, task_id: int) -> None:
        """adds task to open access

        :param task_id: int
            (id of task that will be added to open access)
        :return: None
        """
        self.__state.add_task_to_public(task_id)

    def hide_task(self, task_id: int) -> None:
        """hides task from open access

        :param task_id: int
        :return: None
        """
        self.__state.hide_task(task_id)

    def ban_user(self, ban_data: BanUserModel) -> None:
        """bans user

        :param ban_data: BanUserModel
        :return: None
        """
        self.__state.ban_user(ban_data)

    def edit_another_user(self, user_id: int,
                                 user_update_model: UserUpdateAdminModel) -> None:
        """edits another user using his id

        :param user_id: int
            (id of user that should be edited)
        :param user_update_model: UserUpdateAdminModel
            (new user's data)
        :return: None
        """
        self.__state.edit_another_user(user_id, user_update_model)

    def delete_another_user(self, user: UserTable) -> None:
        """deletes another user

        :param user: UserTable
            (user that should be deleted)
        :return: None
        """
        self.__state.delete_another_user(user)

    def promote_to_default(self, user: UserTable) -> None:
        """promotes user's state to default

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        self.__state.promote_to_default(user)

    def promote_to_helper(self, user: UserTable):
        """promotes user's state to helper

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        self.__state.promote_to_helper(user)

    def promote_to_moderator(self, user: UserTable):
        """promotes user's state to moderator

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        self.__state.promote_to_moderator(user)

    def promote_to_admin(self, user: UserTable):
        """promotes user's state to admin

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        self.__state.promote_to_admin(user)

    def promote_to_elder_admin(self, user: UserTable):
        """promotes user's state to elder admin

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        self.__state.promote_to_elder_admin(user)

    def promote_to_ceo(self, user: UserTable):
        """promotes user's state to ceo

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        self.__state.promote_to_ceo(user)


class UserState:
    """ allows managing user in dependence of his state

    fields
    __user
        user's object of User class
    __user_database
        user's database object
    """
    def __init__(self, user: User, user_database: UserTable):
        self.__user = user
        self.__user_database = user_database

    def get_user_database(self) -> UserTable:
        """gets user's database object

        :return: UserTable
        """
        return self.__user_database

    def get_user(self) -> User:
        """gets user's class object

        :return: User
        """
        return self.__user

    def delete(self) -> None:
        """deletes this user

        :return: None
        """
        raise NotImplementedError

    def update(self, user_update_data: UserUpdateModel) -> None:
        """updates this user data

        :return: None
        """
        raise NotImplementedError

    def show_data(self):
        raise NotImplementedError

    def get_users(self) -> List[UserGetModel]:
        """gets all users from database

        :return: List[UserGetModel]
        """
        raise NotImplementedError

    def get_concrete_user(self, user: UserAbstractModel) -> UserGetModel:
        """gets concrete user

        :param user: UserAbstractModel
            (Model fields for which the search will be performed)
        :return: UserGetModel
        """
        raise NotImplementedError

    def add_task(self, task: TaskAddModel) -> None:
        """adds task to database

        :param task: TaskAddModel
            (Model that contains fields that will have future task)
        :return None
        """
        raise NotImplementedError

    def get_my_tasks(self) -> TaskGetModel:
        """gets all user's tasks

        :return: List[TaskGetModel]
        """
        raise NotImplementedError

    def update_my_task_data(self, task_id: int, task_model: TaskUpdateModel) -> None:
        """updates user's task

        :param task_id: int
            (id of task that will be updated)
        :param task_model: TaskUpdateModel
            (Model that contains new task data)
        :return: None
        """
        raise NotImplementedError

    def delete_my_task(self, task_id: int) -> None:
        """deletes user's task

        :param task_id: int
            (id of task that will be deleted)
        :return: None
        """
        raise NotImplementedError

    def get_task_using_id(self, task_id: int) -> TaskGetModel:
        """gets task using id

        :param task_id: int
            (id of task that will be returned)
        :return: TaskGetModel
        """
        raise NotImplementedError

    def add_task_to_public(self, task_id: int) -> None:
        """adds task to open access

        :param task_id: int
            (id of task that will be added to open access)
        :return: None
        """
        raise NotImplementedError

    def hide_task(self, task_id: int) -> None:
        """hides task from open access

        :param task_id: int
        :return: None
        """
        raise NotImplementedError

    def ban_user(self, ban_data: BanUserModel) -> None:
        """bans user

        :param ban_data: BanUserModel
        :return: None
        """
        raise NotImplementedError

    def edit_another_user(self, user_id: int,
                                 user_update_model: UserUpdateAdminModel) -> None:
        """edits another user using his id

        :param user_id: int
            (id of user that should be edited)
        :param user_update_model: UserUpdateAdminModel
            (new user's data)
        :return: None
        """
        raise NotImplementedError

    def delete_another_user(self, user: UserTable) -> None:
        """deletes another user

        :param user: UserTable
            (user that should be deleted)
        :return: None
        """
        raise NotImplementedError

    def promote_to_helper(self, user: UserTable) -> None:
        """promotes user's state to helper

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        raise NotImplementedError

    def promote_to_moderator(self, user: UserTable) -> None:
        """promotes user's state to moderator

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        raise NotImplementedError

    def promote_to_admin(self, user: UserTable) -> None:
        """promotes user's state to admin

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        raise NotImplementedError

    def promote_to_elder_admin(self, user: UserTable) -> None:
        """promotes user's state to admin

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        raise NotImplementedError

    def promote_to_ceo(self, user: UserTable) -> None:
        """promotes user's state to ceo

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        raise NotImplementedError

    def promote_to_default(self, user: UserTable) -> None:
        """promotes user's state to default

        :param user: UserTable
            (user whose state should be changed)
        :return: None
        """
        raise NotImplementedError


class DefaultState(UserState):

    def update(self, user_update_data: UserUpdateModel):
        session: Session = next(generate_session())
        user = self.get_user_database()
        update_user_data(user, user_update_data, session)

    def delete(self) -> None:
        session: Session = next(generate_session())
        user = self.get_user_database()
        delete_user_from_database(user, session)

    def show_data(self):
        session: Session = next(generate_session())
        user = self.get_user_database()
        return get_user_by_id(user.id, session)

    def get_users(self):
        session: Session = next(generate_session())
        return users_get(session)

    def get_concrete_user(self, user: UserAbstractModel):
        session: Session = next(generate_session())
        return get_user(user, session)

    def add_task(self, task: TaskAddModel):
        session: Session = next(generate_session())
        user = self.get_user_database()
        task_add(task, user, session)

    def get_my_tasks(self):
        user = self.get_user_database()
        return user_tasks_get(user)

    def update_my_task_data(self, task_id: int, task_model: TaskUpdateModel):
        user = self.get_user_database()
        session: Session = next(generate_session())
        update_task_data(task_id, task_model, session, user)

    def delete_my_task(self, task_id: int):
        user = self.get_user_database()
        session: Session = next(generate_session())
        delete_user_task(task_id, user, session)

    def get_task_using_id(self, task_id: int):
        session: Session = next(generate_session())
        return get_task_by_id(task_id, session)


class HelperState(DefaultState):

    def add_task_to_public(self, task_id: int):
        session: Session = next(generate_session())
        task = get_concrete_task_with_every_state(task_id, session)
        task.state = OPEN
        session.commit()

    def hide_task(self, task_id: int):
        session: Session = next(generate_session())
        task = get_task_by_id(task_id, session)
        task.state = HIDDEN
        session.commit()


class ModeratorState(HelperState):

    def ban_user(self, ban_data: BanUserModel):
        session: Session = next(generate_session())
        ban_author = self.get_user_database()
        ban_user_temporary(ban_author, ban_data, session)


class AdminState(ModeratorState):

    def promote_to_default(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_another_state(user, promoter, DEFAULT, session)

    def promote_to_helper(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_another_state(user, promoter, HELPER, session)

    def promote_to_admin(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_another_state(user, promoter, ADMIN, session)

    def promote_to_moderator(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_another_state(user, promoter, MODERATOR, session)

    def ban_user(self, ban_data: BanUserModel):
        session: Session = next(generate_session())
        ban_author = self.get_user_database()
        ban_user_permanently(ban_author, ban_data, session)

    def edit_another_user(self, user_id: int,
                                 user_update_model: UserUpdateAdminModel) -> None:
        session: Session = next(generate_session())
        user = get_user_by_id(user_id, session)
        edit_user(user, user_update_model, session)


class ElderAdminState(AdminState):

    def promote_to_elder_admin(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_another_state(user, promoter, ELDER_ADMIN, session)

    def delete_another_user(self, user: UserTable):
        session: Session = next(generate_session())
        delete_user_from_database(user, session)


class CEOState(ElderAdminState):

    def promote_to_ceo(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_another_state(user, promoter, CEO, session)


class BannedState(UserState):
    pass


states = {
    'default': DefaultState,
    'helper': HelperState,
    'moderator': ModeratorState,
    'admin': AdminState,
    'elder_admin': ElderAdminState,
    'ceo': CEOState,
    'banned': BannedState
}


def convert_string_state_to_class(state: str, user: User,
                                  user_database: UserTable) -> UserState:
    return states[state](user, user_database)

