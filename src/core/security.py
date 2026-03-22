import datetime

import jwt
from passlib.context import CryptContext

from src.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хэширует пароль пользователя"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет совпадение пароля и хэша (для логина)"""
    return pwd_context.verify(plain_password, hashed_password)


PRIVATE_KEY = settings.auth_jwt.private_key_path.read_text()
PUBLIC_KEY = settings.auth_jwt.public_key_path.read_text()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)

    to_encode.update({"exp": expire})

    # Подписываем ПРИВАТНЫМ ключом
    return jwt.encode(
        to_encode,
        PRIVATE_KEY,
        algorithm=settings.auth_jwt.algorithm
    )


def decode_access_token(token: str) -> dict | None:
    try:
        # Проверяем ПУБЛИЧНЫМ ключом
        return jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[settings.auth_jwt.algorithm]
        )
    except jwt.PyJWTError:
        return None
