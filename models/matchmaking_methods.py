from fastapi import HTTPException
from sqlalchemy.orm import Session

from store import User, Staging


def adding_to_staging(user: User, session: Session):
    is_staging_exists = session.query(Staging).filter_by(user_id=user.id).all()
    if is_staging_exists:
        raise HTTPException(status_code=403)
    staging = Staging(
        user_id=user.id
    )
    session.add(staging)
    user.staging.append(staging)
    session.commit()