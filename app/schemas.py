from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class UserOut(UserBase):
    class Config:
        orm_mode = True


class User(UserBase):
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: str | None = None


class BoardBase(BaseModel):
    name: str
    

class BoardCreate(BoardBase):
    pass


class ListBase(BaseModel):
    name: str
    position: int


class ListCreate(ListBase):
    pass


class ListOut(ListBase):
    id: int
    created_at: datetime
    board_id: int

    class Config:
        orm_mode = True


class BoardOut(BoardBase):
    id: int
    owner_id: int
    created_at: datetime

    owner: User
    lists: list[ListOut]

    class Config:
        orm_mode = True


class CardBase(BaseModel):
    title: str
    description: str | None = None
    position: int
    due_date: datetime | None = None


class CardCreate(CardBase):
    pass


class CardOut(CardBase):
    id: int
    list_id: int
    created_at: datetime

    class Config:
        orm_mode = True



class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase):
    id: int
    card_id: int
    created_at: datetime
    updated_at: datetime | None = None

    user: User

    class Config:
        orm_mode = True


