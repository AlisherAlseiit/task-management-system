from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, utils, models


def create_card(db: Session, card: schemas.CardCreate, list_id: int):
    new_card = models.Card(**card.dict(), list_id=list_id)

    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return new_card


def get_cards(db: Session, list_id: int):
    cards = db.query(models.Card).filter(models.Card.list_id == list_id).all()
    return cards


def get_card(db: Session, list_id: int, id: int):
    card = db.query(models.Card).filter(models.Card.list_id == list_id, models.Card.id == id).first()
    return card


def get_card_by_position_and_list_id(db: Session, position: int, list_id: int):
    card = db.query(models.Card).filter(models.Card.position == position, models.Card.list_id == list_id).first()
    return card


def validate_card_presence(db, list_id: int, card_id: int):
    card = get_card(db, list_id, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="card not found")
    return card


def get_card_members(db: Session, card_id: int):
    members = db.query(models.User.id, models.User.username, models.User.email, models.User.created_at).join(models.CardMembers, 
                                                                                                             models.User.id == models.CardMembers.user_id).join(models.Card, 
                                                                                                                                                                models.Card.id == models.CardMembers.card_id).filter(models.CardMembers.card_id == card_id).all()
    return members


def get_card_memeber_by_id(db: Session, card_id: int, member_id: int):
    member = db.query(models.CardMembers).filter(models.CardMembers.card_id == card_id, models.CardMembers.user_id == member_id).first()
    return member


def add_card_member(db: Session, card_id: int, user_id: int):
    new_member = models.CardMembers(user_id=user_id, card_id=card_id)

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


def remove_card_member(db: Session, card_id: int, member_id: int):
    db.query(models.CardMembers).filter(models.CardMembers.card_id == card_id, models.CardMembers.user_id == member_id).delete(synchronize_session=False)
    db.commit()