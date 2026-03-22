import re
from dataclasses import dataclass
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

@dataclass
class UserEntity:
    id: int | None
    email: str
    hashed_password: str
    role: UserRole = UserRole.USER

    def __post_init__(self):
        """
        Бизнес-правила (Инварианты) пользователя.
        Срабатывают автоматически при создании объекта UserEntity(...).
        """
        # 1. Нормализация данных (защита от пробелов и регистра)
        self.email = self.email.lower().strip()

        # 2. Валидация Email (простейшая регулярка)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError(f"Некорректный формат email: {self.email}")

        # 3. Валидация пароля (мы не храним открытый пароль, только хэш)
        if not self.hashed_password:
            raise ValueError("Хэш пароля не может быть пустым")

    def is_admin(self) -> bool:
        """Вспомогательный бизнес-метод"""
        return self.role == UserRole.ADMIN

    def set_role(self, role: UserRole) -> None:
        self.role = role