from core.exceptions.exceptions import not_enough_rights_exception


def throw_exception_if_user_have_no_rights(method, *args):
    try:
        return method(*args)
    except NotImplementedError:
        raise not_enough_rights_exception
