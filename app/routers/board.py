from typing import Annotated


from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..database import get_db
from .. import schemas, oauth2, models, utils
from ..config import settings
from ..crud import users_crud, boards_crud


router = APIRouter(
    prefix="/boards",
    tags=['boards']
)


@router.get("/", response_model=list[schemas.BoardOut])
def get_boards(db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    user_boards = boards_crud.get_boards_by_owner_id(db, current_user.id)
    return user_boards


@router.get("/{board_id}", response_model=schemas.BoardOut)
def get_board(board_id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.get_board_by_id(db, board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="permission denied")
    
    return board


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BoardOut)
def create_board(board: schemas.BoardCreate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    new_board = boards_crud.create_board(db, board, current_user.id)
    return new_board




    






    










