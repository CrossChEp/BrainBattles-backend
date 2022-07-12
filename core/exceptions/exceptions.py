from fastapi import HTTPException

not_enough_rights_exception = HTTPException(
    status_code=403,
    detail="You haven't got enough rights"
)

cannot_make_action_with_this_user = HTTPException(
    status_code=403,
    detail="You can't make this action with this user as his state is greater then your"
)
