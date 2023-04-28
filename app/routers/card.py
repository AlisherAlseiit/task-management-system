from typing import Annotated

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, oauth2, models, utils
from ..crud import users_crud, boards_crud, lists_crud, cards_crud


router = APIRouter(
    prefix="/boards",
    tags=['cards']
)


@router.get("/{board_id}/lists/{list_id}/cards", response_model=list[schemas.CardOut])
def get_cards(board_id: int, list_id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)
    cards = cards_crud.get_cards(db, list_id)

    return cards


@router.get("/{board_id}/lists/{list_id}/cards/{card_id}", response_model=schemas.CardOut)
def get_card(board_id: int, list_id: int, card_id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)
    card = cards_crud.validate_card_presence(db, list_id, card_id)
    
    return card


@router.post("/{board_id}/lists/{list_id}/cards", response_model=schemas.CardOut)
def create_card(board_id: int, list_id: int, card: schemas.CardCreate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)

    unique_card = cards_crud.get_card_by_position_and_list_id(db, card.position, list_id)
    if unique_card:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="card with this position already exists")

    new_card = cards_crud.create_card(db, card, list_id)

    return new_card