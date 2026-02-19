"""Контроллер - оркестрация операций и обработка ошибок"""
import schedule
import time
import logging

from domain.exceptions import ConnectionTimeoutError, ConnectionFailedError, ApiErrorResponseError, \
    InvalidApiResponseError, ValidationError, RepositoryError, CurrencyTrackerError
from services.currency_service import CurrencyService

logger = logging.getLogger(__name__)


class SchedulerController:
    """Контроллер для периодического выполнения задач"""

    def __init__(self, currency_service: CurrencyService, interval_minutes: int = 5):
        self._currency_service = currency_service
        self._interval_minutes = interval_minutes
        self._job = None

    def start(self) -> None:
        """Запуск планировщика с обработкой ошибок на уровне контроллера"""
        self._job = schedule.every(self._interval_minutes).minutes.do(self._scheduled_task)

        logger.info(f"Планировщик запущен. Запросы каждые {self._interval_minutes} минут")
        logger.info("Для остановки нажмите Ctrl+C")

        self._scheduled_task()

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹Планировщик остановлен пользователем")

    def _scheduled_task(self) -> None:
        """Задача по расписанию с полной обработкой ошибок"""
        logger.info("Выполнение запланированного запроса курсов валют...")

        try:
            rate = self._currency_service.fetch_and_save_rates("EUR")

            logger.info(
                f"Успешно сохранен курс {rate.base_currency}/{rate.target_currency} = "
                f"{rate.rate} на {rate.date}"
            )

        except ConnectionTimeoutError as e:
            logger.error(f"Таймаут подключения: {e}", exc_info=True)

        except ConnectionFailedError as e:
            logger.error(f"Ошибка подключения: {e}", exc_info=True)

        except ApiErrorResponseError as e:
            logger.error(f"API вернул ошибку: {e}", exc_info=True)

        except InvalidApiResponseError as e:
            logger.error(f"Некорректный ответ API: {e}", exc_info=True)

        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}", exc_info=True)

        except RepositoryError as e:
            logger.error(f"Ошибка сохранения в БД: {e}", exc_info=True)

        except CurrencyTrackerError as e:
            logger.error(f"Ошибка бизнес-логики: {e}", exc_info=True)

        except Exception as e:
            logger.critical(
                f"Критическая необработанная ошибка: {type(e).__name__}: {e}",
                exc_info=True
            )