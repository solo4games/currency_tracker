"""Кастомные исключения приложения"""
from typing import Optional


class CurrencyTrackerError(Exception):
    """Базовое исключение приложения"""
    pass


class GatewayError(CurrencyTrackerError):
    """Ошибка шлюза (внешнего API)"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class ConnectionTimeoutError(GatewayError):
    """Таймаут подключения к внешнему API"""
    pass


class ConnectionFailedError(GatewayError):
    """Ошибка подключения к внешнему API"""
    pass


class ApiErrorResponseError(GatewayError):
    """API вернул ошибочный HTTP статус"""
    def __init__(self, status_code: int, message: str):
        super().__init__(f"API вернул статус {status_code}: {message}")
        self.status_code = status_code


class InvalidApiResponseError(GatewayError):
    """Некорректный формат ответа API"""
    pass


class RepositoryError(CurrencyTrackerError):
    """Ошибка репозитория (БД)"""
    pass


class ValidationError(CurrencyTrackerError):
    """Ошибка валидации данных"""
    pass