from abc import ABC, abstractmethod
from decimal import Decimal


class IPaymentGateway(ABC):
    @abstractmethod
    async def charge(self, amount: Decimal, currency: str, token: str) -> bool:
        """Метод для списания денег"""
        pass