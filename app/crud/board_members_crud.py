from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, utils, models


def get_board_members(db: Session, board_id: int):
    board_members = db.query(models.BoardMember).filter(models.BoardMember.board_id == board_id).all()
    return board_members


def get_board_member(db: Session, board_id: int, user_id: int):
    board_member = db.query(models.BoardMember).filter(models.BoardMember.board_id == board_id, models.BoardMember.user_id == user_id).first()
    return board_member


def add_board_member(db: Session, board_id: int, user_id: int):
    board_member = models.BoardMember(board_id=board_id, user_id=user_id)

    db.add(board_member)
    db.commit()
    db.refresh(board_member)


def update_board_member(db: Session, board_id: int, user_id: int, updated_member: schemas.BoardMemberUpdate):
    db.query(models.BoardMember).filter(models.BoardMember.board_id == board_id, models.BoardMember.user_id == user_id).update({"role": updated_member.role}, synchronize_session=False)
    db.commit()


def remove_board_member(db: Session, board_id: int, user_id: int):
    db.query(models.BoardMember).filter(models.BoardMember.board_id == board_id, models.BoardMember.user_id == user_id).delete(synchronize_session=False)
    db.commit()