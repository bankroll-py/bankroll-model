from abc import ABC, abstractmethod
from typing import Any, List


class ConvertableModel(ABC):
    @staticmethod
    @abstractmethod
    def dataframeColumns() -> List[str]:
        pass

    @abstractmethod
    def dataframeValues(self) -> List[Any]:
        pass
