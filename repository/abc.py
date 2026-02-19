from abc import ABC, abstractmethod
from typing import List, Optional

from models import Request, Response


class IRequestRepository(ABC):
    @abstractmethod
    def create(self, endpoint: str, status_code: Optional[int] = None,
               error_message: Optional[str] = None) -> Request:
        """
        Создается Response
        """

    @abstractmethod
    def get_by_id(self, request_id: int) -> Optional[Request]:
        """
        Создается Response
        """


class IResponseRepository(ABC):
    @abstractmethod
    def create(self, request_id: int, base_currency: str, target_currency: str,
               rate: float, date: str, raw_data: str) -> Response:
        """
        Создается Response
        """

    @abstractmethod
    def get_history_with_requests(self, limit: int = 100) -> List[dict]:
        """
        Возвращает историю с JOIN между requests и responses
        """