from fastapi import HTTPException
from sqlalchemy.orm import Session

from store import User, Staging


def adding_to_staging(subject: str, user: User, session: Session):
    is_staging_exists = session.query(Staging).filter_by(user_id=user.id).all()
    if is_staging_exists:
        raise HTTPException(status_code=403, detail='User already in staging')
    staging = Staging(
        user_id=user.id,
        rank=user.rank,
        subject=subject
    )
    session.add(staging)
    user.staging.append(staging)
    session.commit()


def delete_from_staging(user: User, session: Session):
    staging = session.query(Staging).filter_by(user_id=user.id).first()
    if not staging:
        raise HTTPException(status_code=403, detail='User is not in staging')
    session.delete(staging)
    session.commit()