"""Сервис содержит ТОЛЬКО бизнес-логику, без деталей реализации"""
import logging
from typing import List

from domain.entities import CurrencyRate, ExchangeRatesResponse
from domain.exceptions import ValidationError
from gateways.abc import CurrencyGateway
from repository.abc import IRequestRepository, IResponseRepository

logger = logging.getLogger(__name__)


class CurrencyService:
    """
    Сервис для работы с курсами валют.
    Содержит бизнес-логику без зависимостей от инфраструктуры.
    """

    def __init__(
            self,
            gateway: CurrencyGateway,
            request_repo: IRequestRepository,
            response_repo: IResponseRepository
    ):
        self._gateway = gateway
        self._request_repo = request_repo
        self._response_repo = response_repo

    def fetch_and_save_rates(self, target_currency: str = "EUR") -> CurrencyRate:
        """
        Бизнес-операция: получить и сохранить курс валюты

        Args:
            target_currency: Код целевой валюты (например, "EUR")

        Returns:
            CurrencyRate: Сохраненный курс валюты

        Raises:
            ValidationError: Некорректный код валюты
            CurrencyTrackerError: Любая ошибка при выполнении операции
        """

        if not target_currency or len(target_currency) != 3:
            raise ValidationError(
                f"Код валюты должен быть 3-символьным, получено: '{target_currency}'"
            )

        logger.info(f"Начало операции: получение курса USD -> {target_currency}")

        exchange_response = self._gateway.fetch_rates(base_currency="USD")

        try:
            rate = exchange_response.get_rate(target_currency)
        except KeyError as e:
            raise ValidationError(
                f"Валюта {target_currency} недоступна в ответе API"
            ) from e

        self._save_to_database(exchange_response, rate)

        logger.info(
            f"Операция завершена успешно: {rate.base_currency} -> "
            f"{rate.target_currency} = {rate.rate} ({rate.date})"
        )
        return rate

    def get_history(self, limit: int = 100) -> List[dict]:
        """
        Получить историю запросов с ответами

        Returns:
            Список словарей с данными из БД (результат JOIN)
        """
        return self._response_repo.get_history_with_requests(limit)

    def _save_to_database(self, exchange_response: ExchangeRatesResponse, rate: CurrencyRate) -> None:
        """Внутренний метод для сохранения данных в БД"""
        request = self._request_repo.create(
            endpoint=f"/latest/{exchange_response.base}",
            status_code=200
        )

        self._response_repo.create(
            request_id=request.id,
            base_currency=rate.base_currency,
            target_currency=rate.target_currency,
            rate=rate.rate,
            date=rate.date,
            raw_data=exchange_response.raw_data
        )