from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, utils, models


def create_board(db: Session, board: schemas.BoardCreate, owner_id: int):
    new_board = models.Board(owner_id=owner_id, **board.dict())

    db.add(new_board)
    db.commit()
    db.refresh(new_board)

    return new_board


def get_boards_by_owner_id(db: Session, owner_id: int):
    boards = db.query(models.Board).filter(models.Board.owner_id == owner_id).all()
    return boards


def get_board_by_id(db: Session, id: int):
    board = db.query(models.Board).filter(models.Board.id == id).first()
    return board


def validate_board_presence(db: Session, board_id: int):
    board = get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="board not found")
    return board

