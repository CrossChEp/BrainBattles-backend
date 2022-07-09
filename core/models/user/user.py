from sqlalchemy.orm import Session
from tornado.process import task_id

from core.configs.config import HIDDEN, OPEN
from core.middlewares.database_session import generate_session
from core.models import task_add, user_tasks_get, update_task_data, get_task_by_id, get_concrete_task_with_every_state
from core.models.tasks.tasks_methods import delete_user_task
from core.models.user.user_methods import update_user_data, delete_user_from_database, get_user_by_id, get_user, users_get
from core.schemas import UserAbstractModel, UserUpdateModel, TaskAddModel, TaskUpdateModel
from core.store import UserTable, TaskTable


class User:

    def __init__(self, user: UserTable):
        self.__user: UserTable = user
        self.__state: UserState = convert_string_state_to_class(
            state=user.state,
            user=self,
            user_database=self.__user
        )

    def delete(self):
        self.__state.delete()

    def update(self, user_update_data: UserUpdateModel):
        self.__state.update(user_update_data)

    def get_users(self):
        return self.__state.get_users()

    def get_user(self, user: UserAbstractModel):
        return self.__state.get_concrete_user(user)

    def add_task(self, task: TaskAddModel):
        self.__state.add_task(task)

    def get_my_tasks(self):
        return self.__state.get_my_tasks()

    def update_my_task_data(self, task_id: int, task_model: TaskUpdateModel):
        self.__state.update_my_task_data(task_id, task_model)

    def delete_my_task(self, task_id: int):
        self.__state.delete_my_task(task_id)

    def get_task_using_id(self, task_id: int):
        return self.__state.get_task_using_id(task_id)

    def add_task_to_public(self, task_id: int):
        self.__state.add_task_to_public(task_id)

    def hide_task(self, task_id: int):
        self.__state.hide_task(task_id)


class UserState:

    def __init__(self, user: User, user_database: UserTable):
        self.__user = user
        self.__user_database = user_database

    def get_user_database(self):
        return self.__user_database

    def get_user(self):
        return self.__user

    def delete(self):
        raise NotImplementedError

    def update(self, user_update_data: UserUpdateModel):
        raise NotImplementedError

    def show_data(self):
        raise NotImplementedError

    def get_users(self):
        raise NotImplementedError

    def get_concrete_user(self, user: UserAbstractModel):
        raise NotImplementedError

    def add_task(self, task: TaskAddModel):
        raise NotImplementedError

    def get_my_tasks(self):
        raise NotImplementedError

    def update_my_task_data(self, task_id: int, task_model: TaskUpdateModel):
        raise NotImplementedError

    def delete_my_task(self, task_id: int):
        raise NotImplementedError

    def get_task_using_id(self, task_id: int):
        raise NotImplementedError

    def add_task_to_public(self, task_id: int):
        raise NotImplementedError

    def hide_task(self, task_id: int):
        raise NotImplementedError


class DefaultState(UserState):

    def update(self, user_update_data: UserUpdateModel):
        session: Session = next(generate_session())
        user = self.get_user_database()
        update_user_data(user, user_update_data, session)

    def delete(self):
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


class ModeratorState(UserState):
    pass


class AdminState(UserState):
    pass


class ElderAdminState(UserState):
    pass


class CEOState(UserState):
    pass


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

