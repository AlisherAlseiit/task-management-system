from typing import Annotated

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, oauth2
from ..crud import users_crud


router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    unique_user = users_crud.get_user_by_email(db, user.email)
    if unique_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"this email already exists")
    
    unique_username = users_crud.get_user_by_username(db, user.username)
    if unique_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is taken")
    
    new_user = users_crud.create_user(db, user)
    
    return new_user


@router.get("/", response_model=list[schemas.UserOut])
async def get_users(db: Annotated[Session, Depends(get_db)]):
    users = users_crud.get_users(db)
    return users