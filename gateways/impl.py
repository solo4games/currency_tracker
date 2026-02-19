"""Реализации шлюзов"""
import requests
import json
import logging
from typing import Dict
from requests.exceptions import Timeout, ConnectionError as RequestsConnectionError

from domain.entities import ExchangeRatesResponse
from domain.exceptions import ApiErrorResponseError, InvalidApiResponseError, ConnectionTimeoutError, \
    ConnectionFailedError
from gateways.abc import CurrencyGateway

logger = logging.getLogger(__name__)


class CurrencyHttpGateway(CurrencyGateway):
    """HTTP реализация шлюза для exchangerate-api.com"""

    def __init__(self, base_url: str, timeout: int = 10):
        self._base_url = base_url
        self._timeout = timeout

    def fetch_rates(self, base_currency: str = "USD") -> ExchangeRatesResponse:
        url = f"{self._base_url}/{base_currency}"

        try:
            logger.debug(f"HTTP GET запрос к {url}")
            response = requests.get(url, timeout=self._timeout)

            if response.status_code != 200:
                raise ApiErrorResponseError(
                    status_code=response.status_code,
                    message=response.text[:500]
                )

            try:
                data: Dict = response.json()
            except json.JSONDecodeError as e:
                raise InvalidApiResponseError(
                    f"Невозможно распарсить JSON ответ: {e}"
                )

            required_fields = ["base", "date", "rates"]
            missing = [f for f in required_fields if f not in data]
            if missing:
                raise InvalidApiResponseError(
                    f"В ответе API отсутствуют обязательные поля: {missing}"
                )

            exchange_response = ExchangeRatesResponse(
                base=data["base"],
                date=data["date"],
                rates=data["rates"],
                raw_data=json.dumps(data)
            )

            logger.info(
                f"Успешно получен курс {exchange_response.base} -> "
                f"{len(exchange_response.rates)} валют на дату {exchange_response.date}"
            )
            return exchange_response

        except Timeout as e:
            raise ConnectionTimeoutError(
                f"Таймаут подключения к {url} ({self._timeout} сек)",
                original_error=e
            )

        except RequestsConnectionError as e:
            raise ConnectionFailedError(
                f"Ошибка подключения к {url}: {str(e)}",
                original_error=e
            )

        except requests.RequestException as e:
            raise ConnectionFailedError(
                f"Неизвестная ошибка запроса к {url}: {str(e)}",
                original_error=e
            )