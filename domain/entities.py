"""Доменные сущности - чистая бизнес-логика без зависимостей от фреймворков"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass(frozen=True)
class CurrencyRate:
    """Курс валюты от базовой"""
    base_currency: str
    target_currency: str
    rate: float
    date: str

    def __post_init__(self):
        if not self.base_currency or len(self.base_currency) != 3:
            raise ValueError(f"Некорректная базовая валюта: {self.base_currency}")
        if not self.target_currency or len(self.target_currency) != 3:
            raise ValueError(f"Некорректная целевая валюта: {self.target_currency}")
        if self.rate <= 0:
            raise ValueError(f"Курс валюты должен быть положительным: {self.rate}")


@dataclass(frozen=True)
class ExchangeRatesResponse:
    """Полный ответ API с курсами валют"""
    base: str
    date: str
    rates: Dict[str, float]
    raw_data: str

    @property
    def timestamp(self) -> datetime:
        return datetime.strptime(self.date, "%Y-%m-%d")

    def get_rate(self, currency: str) -> CurrencyRate:
        """Получить курс для конкретной валюты"""
        if currency not in self.rates:
            raise KeyError(f"Валюта {currency} отсутствует в ответе")
        return CurrencyRate(
            base_currency=self.base,
            target_currency=currency,
            rate=self.rates[currency],
            date=self.date
        )


@dataclass
class ApiRequest:
    """Информация о запросе к внешнему API"""
    endpoint: str
    timestamp: datetime
    status_code: Optional[int] = None
    error_message: Optional[str] = None