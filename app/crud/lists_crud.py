from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, utils, models


def create_list(db: Session, list: schemas.ListCreate, board_id: int):
    new_list = models.List(**list.dict(), board_id=board_id)

    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return new_list


def get_lists_by_board_id(db: Session, board_id: int):
    lists = db.query(models.List).filter(models.List.board_id == board_id).all()
    return lists


def get_list(db: Session, board_id: int, id: int):
    list = db.query(models.List).filter(models.List.board_id == board_id, models.List.id == id).first()
    return list


def get_list_by_position_and_board_id(db: Session, position: int, board_id: int):
    list = db.query(models.List).filter(models.List.position == position, models.List.board_id == board_id).first()
    return list


def validate_list_presence(db, board_id: int, list_id: int):
    list = get_list(db, board_id, list_id)
    if not list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="list not found") 
    return list