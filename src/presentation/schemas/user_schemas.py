from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.domain.entity.user_entity import UserRole



class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50, description="Пароль пользователя")


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole # todo убрать потом

    # Эта магия позволяет Pydantic'у читать данные из нашего класса UserEntity
    model_config = ConfigDict(from_attributes=True)