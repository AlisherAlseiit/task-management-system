from typing import Annotated

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, oauth2, models, utils
from ..crud import users_crud, boards_crud, lists_crud


router = APIRouter(
    prefix="/boards",
    tags=['lists']
)


@router.get("/{board_id}/lists", response_model=list[schemas.ListOut])
def get_lists(board_id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value])
    lists = lists_crud.get_lists_by_board_id(db, board_id)

    return lists


@router.get("/{board_id}/lists/{list_id}", response_model=schemas.ListOut)
def get_list(board_id: int, list_id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value])
    list = lists_crud.validate_list_presence(db, board_id, list_id)
    
    return list


@router.post("/{board_id}/lists", status_code=status.HTTP_201_CREATED, response_model=schemas.ListOut)
def create_list(board_id: int, list: schemas.ListCreate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value])

    unique_list = lists_crud.get_list_by_position_and_board_id(db, list.position, board_id)
    if unique_list:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="list with this position already exists")
    
    new_list = lists_crud.create_list(db, list, board_id)

    return new_list