from sqlalchemy.orm import Session

from core.middlewares.database_session import generate_session
from core.models.user.user_methods import update_user_data, delete_user_from_database, get_user_by_id, get_user, users_get
from core.schemas import UserAbstractModel, UserUpdateModel
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

    def update(self):
        pass

    def show_data(self):
        pass

    def get_users(self):
        return self.__state.get_users()

    def get_user(self, user: UserAbstractModel):
        pass


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


class HelperState(UserState):
    pass


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

