from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class EventEntity:
    id: int | None
    title: str
    event_date: datetime
    location: str

    def __post_init__(self):
        """
        Бизнес-правила мероприятия.
        """
        # 1. Очистка от лишних пробелов
        self.title = self.title.strip()
        self.location = self.location.strip()

        # 2. Проверка заполненности
        if not self.title:
            raise ValueError("Название мероприятия не может быть пустым")

        if not self.location:
            raise ValueError("Место проведения не может быть пустым")

        # 3. Работа со временем (САМОЕ ВАЖНОЕ В ЭТОМ ПРОЕКТЕ)
        # Если дата пришла без таймзоны (naive), принудительно ставим UTC
        if self.event_date.tzinfo is None:
            self.event_date = self.event_date.replace(tzinfo=timezone.utc)

        current_time = datetime.now(timezone.utc)

        # 4. Проверка даты (Нельзя создать концерт, который уже прошел)
        if self.event_date <= current_time:
            raise ValueError("Дата мероприятия должна быть в будущем")
