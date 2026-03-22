from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum


class TicketStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    PAID = "PAID"

@dataclass
class TicketEntity:
    id: int | None

    reserved_by_user_id: int | None
    reserved_until: datetime | None

    event_id: int
    seat_number: int
    price: Decimal
    status: TicketStatus

    def reserve(self, user_id: int, current_time: datetime):
        """Правило бронирования"""
        # Если билет куплен — отказ
        if self.status == TicketStatus.PAID:
            raise ValueError("Билет уже выкуплен")

        # Если билет забронирован кем-то другим и время брони еще не вышло — отказ
        if self.reserved_until and self.reserved_until.tzinfo is None:
            self.reserved_until = self.reserved_until.replace(tzinfo=timezone.utc)

            # Теперь сравнение с current_time (которое тоже в UTC) сработает!
        if self.status == TicketStatus.RESERVED and self.reserved_until > current_time:
            raise ValueError("Билет временно забронирован другим пользователем")

        # Если всё ок — бронируем на 15 минут
        self.status = TicketStatus.RESERVED
        self.reserved_by_user_id = user_id
        self.reserved_until = current_time + timedelta(minutes=15)

    def pay(self, user_id: int, current_time: datetime):
        """Правило оплаты"""
        if self.status != TicketStatus.RESERVED:
            raise ValueError("Билет нужно сначала забронировать")

        if self.reserved_by_user_id != user_id:
            raise ValueError("Это не ваша бронь")

        if self.reserved_until < current_time:
            # Бронь сгорела!
            self.status = TicketStatus.AVAILABLE
            self.reserved_by_user_id = None
            raise ValueError("Время бронирования истекло")

        self.status = TicketStatus.PAID
