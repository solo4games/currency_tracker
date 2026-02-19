from sqlalchemy.orm import Session
from sqlalchemy import select, join
from typing import List, Optional

from models import Request, Response
from repository.abc import IRequestRepository, IResponseRepository


class SQLAlchemyRequestRepository(IRequestRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, endpoint: str, status_code: Optional[int] = None,
               error_message: Optional[str] = None) -> Request:
        request = Request(
            endpoint=endpoint,
            status_code=status_code,
            error_message=error_message
        )
        self._session.add(request)
        self._session.commit()
        return request

    def get_by_id(self, request_id: int) -> Optional[Request]:
        return self._session.get(Request, request_id)


class SQLAlchemyResponseRepository(IResponseRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, request_id: int, base_currency: str, target_currency: str,
               rate: float, date: str, raw_data: str) -> Response:
        response = Response(
            request_id=request_id,
            base_currency=base_currency,
            target_currency=target_currency,
            rate=rate,
            date=date,
            raw_data=raw_data
        )
        self._session.add(response)
        self._session.commit()
        return response

    def get_history_with_requests(self, limit: int = 100) -> List[dict]:
        stmt = (
            select(
                Request.id.label("request_id"),
                Request.timestamp,
                Request.endpoint,
                Request.status_code,
                Response.id.label("response_id"),
                Response.base_currency,
                Response.target_currency,
                Response.rate,
                Response.date.label("exchange_date"),
                Response.raw_data
            )
            .select_from(
                join(Request, Response, Request.id == Response.request_id)
            )
            .order_by(Request.timestamp.desc())
            .limit(limit)
        )

        result = self._session.execute(stmt)
        return [
            {
                "request_id": row.request_id,
                "timestamp": row.timestamp.isoformat(),
                "endpoint": row.endpoint,
                "status_code": row.status_code,
                "response_id": row.response_id,
                "base_currency": row.base_currency,
                "target_currency": row.target_currency,
                "rate": float(row.rate),
                "exchange_date": row.exchange_date,
                "raw_data": row.raw_data
            }
            for row in result
        ]