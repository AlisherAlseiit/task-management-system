from enum import Enum

from passlib.context import CryptContext


pwd_contenxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_contenxt.hash(password)


def verify(plain_password, hash_password):
    return pwd_contenxt.verify(plain_password, hash_password)