
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, utils, models


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def get_user_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


def get_users(db: Session):
    users = db.query(models.User).all()
    return users


def create_user(db: Session, user: schemas.UserCreate):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_board_member(db: Session, user_id: int, board_id):
    user = db.query(models.BoardMember).filter(models.BoardMember.user_id == user_id, models.BoardMember.board_id == board_id).first()
    return user


def check_board_permissions(db, board, user_id, roles: list[str]):
    if board.owner_id != user_id:
        board_member = get_board_member(db, user_id, board.id)
        if not board_member or board_member.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="permission denied")
