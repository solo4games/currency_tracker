"""Абстракции шлюзов для внешних сервисов"""
from abc import ABC, abstractmethod

from domain.entities import ExchangeRatesResponse


class CurrencyGateway(ABC):
    """Абстракция шлюза для получения курсов валют"""

    @abstractmethod
    def fetch_rates(self, base_currency: str = "USD") -> ExchangeRatesResponse:
        """
        Получить курсы валют от базовой валюты

        Raises:
            ConnectionTimeoutError: Таймаут подключения
            ConnectionFailedError: Ошибка сети
            ApiErrorResponseError: Ошибочный HTTP статус
            InvalidApiResponseError: Некорректный формат ответа
        """
        pass