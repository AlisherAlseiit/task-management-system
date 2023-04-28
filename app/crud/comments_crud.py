from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, utils, models


def create_comment(db: Session, comment: schemas.CommentCreate, card_id: int, user_id: int):
    new_comment = models.Comment(**comment.dict(), card_id=card_id, user_id=user_id)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def get_comments(db: Session, card_id: int):
    comments = db.query(models.Comment).filter(models.Comment.card_id == card_id).all()
    return comments


def get_user_comment(db: Session, card_id: int, comment_id: int, user_id: int):
    comment = db.query(models.Comment).filter(models.Comment.card_id == card_id, models.Comment.id == comment_id, models.Comment.user_id == user_id).first()
    return comment


def delete_comment(db: Session, comment_id: int):
    db.query(models.Comment).filter(models.Comment.id == comment_id).delete(synchronize_session=False)
    db.commit()