from typing import Annotated

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, oauth2, models, utils
from ..crud import users_crud, boards_crud, lists_crud, cards_crud, comments_crud


router = APIRouter(
    prefix="/boards",
    tags=['comments']
)


@router.post("/{board_id}/lists/{list_id}/cards/{card_id}/comments", response_model=schemas.CommentOut)
def create_comment(board_id: int, 
                    list_id: int,
                    card_id: int, 
                    comment: schemas.CommentCreate,
                    db: Annotated[Session, Depends(get_db)], 
                    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)
    _ = cards_crud.validate_card_presence(db, list_id, card_id)
    new_comment = comments_crud.create_comment(db, comment, card_id, current_user.id)

    return new_comment


@router.get("/{board_id}/lists/{list_id}/cards/{card_id}/comments", response_model=list[schemas.CommentOut])
def get_comments(board_id: int, 
                   list_id: int,
                   card_id: int,
                   db: Annotated[Session, Depends(get_db)], 
                   current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value, utils.Roles.OBSERVER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)
    _ = cards_crud.validate_card_presence(db, list_id, card_id)
    comments = comments_crud.get_comments(db, card_id)

    return comments


@router.delete("/{board_id}/lists/{list_id}/cards/{card_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def get_comments(board_id: int, 
                   list_id: int,
                   card_id: int,
                   comment_id: int,
                   db: Annotated[Session, Depends(get_db)], 
                   current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)
    _ = cards_crud.validate_card_presence(db, list_id, card_id)

    comment = comments_crud.get_user_comment(db, card_id, comment_id, current_user.id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    comments_crud.delete_comment(db, comment_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{board_id}/lists/{list_id}/cards/{card_id}/comments/{comment_id}", response_model=schemas.CommentOut)
def get_comments(board_id: int, 
                   list_id: int,
                   card_id: int,
                   comment_id: int,
                   updated_comment: schemas.CommentCreate,
                   db: Annotated[Session, Depends(get_db)], 
                   current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)]):
    board = boards_crud.validate_board_presence(db, board_id)
    users_crud.check_board_permissions(db, board, current_user.id, roles=[utils.Roles.ADMIN.value, utils.Roles.MEMBER.value])
    _ = lists_crud.validate_list_presence(db, board_id, list_id)
    _ = cards_crud.validate_card_presence(db, list_id, card_id)
    
    comment = comments_crud.get_user_comment(db, card_id, comment_id, current_user.id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    comments_crud.update_comment(db, updated_comment, comment_id)
    return comment

    
