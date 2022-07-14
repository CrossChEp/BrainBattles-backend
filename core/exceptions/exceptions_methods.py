from core.configs import states
from core.exceptions.exceptions import not_enough_rights_exception, cannot_make_action_with_this_user
from core.store import UserTable


def throw_exception_if_user_have_no_rights(method, *args):
    try:
        return method(*args)
    except NotImplementedError:
        raise not_enough_rights_exception


def throw_exception_if_user_have_lesser_state(user: UserTable, action_user: UserTable):
    if states.index(user.state) < states.index(action_user.state):
        raise cannot_make_action_with_this_user
