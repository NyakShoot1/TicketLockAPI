from abc import ABC, abstractmethod, _T


class BaseEntity(ABC):

    @abstractmethod
    def entity_to_model(self) -> _T:
        raise NotImplementedError()

