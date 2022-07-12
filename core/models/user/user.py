from sqlalchemy.orm import Session

from core.configs import DEFAULT, HELPER, MODERATOR, ADMIN, ELDER_ADMIN, CEO
from core.configs.config import HIDDEN, OPEN
from core.middlewares.database_session import generate_session
from core.models import task_add, user_tasks_get, update_task_data, get_task_by_id, get_concrete_task_with_every_state
from core.models.admin.users.admin_users_methods import ban_user_temporary, ban_user_permanently, edit_user, \
    promote_user_to_anther_state
from core.models.tasks.tasks_methods import delete_user_task
from core.models.user.user_methods import update_user_data, delete_user_from_database, get_user_by_id, get_user, users_get
from core.schemas import UserAbstractModel, UserUpdateModel, TaskAddModel, TaskUpdateModel, BanUserModel, \
    UserUpdateAdminModel
from core.store import UserTable


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

    def ban_user(self, ban_data: BanUserModel):
        self.__state.ban_user(ban_data)

    def edit_another_user(self, user_id: int,
                                 user_update_model: UserUpdateAdminModel):
        self.__state.edit_another_user(user_id, user_update_model)

    def delete_another_user(self, user: UserTable):
        self.__state.delete_another_user(user)

    def promote_to_helper(self, user: UserTable):
        self.__state.promote_to_helper(user)

    def promote_to_moderator(self, user: UserTable):
        self.__state.promote_to_moderator(user)

    def promote_to_admin(self, user: UserTable):
        self.__state.promote_to_admin(user)

    def promote_to_elder_admin(self, user: UserTable):
        self.__state.promote_to_elder_admin(user)

    def promote_to_ceo(self, user: UserTable):
        self.__state.promote_to_ceo(user)

    def promote_to_default(self, user: UserTable):
        self.__state.promote_to_default(user)


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

    def ban_user(self, ban_data: BanUserModel):
        raise NotImplementedError

    def edit_another_user(self, user_id: int,
                                 user_update_model: UserUpdateAdminModel) -> None:
        raise NotImplementedError

    def delete_another_user(self, user: UserTable):
        raise NotImplementedError

    def promote_to_helper(self, user: UserTable):
        raise NotImplementedError

    def promote_to_moderator(self, user: UserTable):
        raise NotImplementedError

    def promote_to_admin(self, user: UserTable):
        raise NotImplementedError

    def promote_to_elder_admin(self, user: UserTable):
        raise NotImplementedError

    def promote_to_ceo(self, user: UserTable):
        raise NotImplementedError

    def promote_to_default(self, user: UserTable):
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
        promote_user_to_anther_state(user, promoter, DEFAULT, session)

    def promote_to_helper(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_anther_state(user, promoter, HELPER, session)

    def promote_to_admin(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_anther_state(user, promoter, ADMIN, session)

    def promote_to_moderator(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_anther_state(user, promoter, MODERATOR, session)

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
        promote_user_to_anther_state(user, promoter, ELDER_ADMIN, session)

    def delete_another_user(self, user: UserTable):
        session: Session = next(generate_session())
        delete_user_from_database(user, session)


class CEOState(ElderAdminState):

    def promote_to_ceo(self, user: UserTable):
        session: Session = next(generate_session())
        user = get_user_by_id(user.id, session)
        promoter = self.get_user_database()
        promote_user_to_anther_state(user, promoter, CEO, session)


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

