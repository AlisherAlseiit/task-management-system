from sqlalchemy.orm import Session

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


def create_list(db: Session, list: schemas.ListCreate, board_id: int):
    new_list = models.List(**list.dict(), board_id=board_id)

    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return new_list



def get_lists(db: Session):
    lists = db.query(models.List).all()
    return lists


def get_list(db: Session, id: int):
    list = db.query(models.List).filter(models.List.id == id).first()
    return list