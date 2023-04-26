from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, Table
from sqlalchemy.orm import relationship

from .database import Base


CardMembers = Table('card_members', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    boards = relationship('Board', back_populates='owner')
    cards = relationship('Card', secondary=CardMembers, back_populates='users')
    comments = relationship('Comment', back_populates='user')


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner = relationship('User', back_populates='boards')
    lists = relationship('List', back_populates='board')


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    position = Column(Integer, nullable=False, unique=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    board = relationship('Board', back_populates='lists')
    cards = relationship('Card', back_populates='list')


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    position = Column(Integer, nullable=False, unique=True)
    due_date = Column(TIMESTAMP(timezone=True))
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    list = relationship('List', back_populates='cards')
    users = relationship('User', secondary=CardMembers, back_populates='cards')
    comments = relationship('Comment', back_populates="card")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    comment_text = Column(String, nullable=False)
    card_id = Column(Integer, ForeignKey('cards.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)

    card = relationship('Card', back_populates='comments')
    user = relationship('User', back_populates='comments')


class BoardMember(Base):
    __tablename__ = "board_members"

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    board_id = Column(Integer, ForeignKey('boards.id', ondelete='CASCADE'), primary_key=True)
    role = Column(String, nullable=False, server_default="observer")
