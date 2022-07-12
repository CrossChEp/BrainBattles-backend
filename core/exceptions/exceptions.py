from fastapi import HTTPException

not_enough_rights_exception = HTTPException(
    status_code=403,
    detail="You haven't got enough rights"
)
