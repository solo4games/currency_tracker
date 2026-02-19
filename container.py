import punq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from controllers.scheduler_controller import SchedulerController
from gateways.abc import CurrencyGateway
from gateways.impl import CurrencyHttpGateway
from models import Base
from repository.abc import IRequestRepository, IResponseRepository
from repository.impl import SQLAlchemyRequestRepository, SQLAlchemyResponseRepository
from services.currency_service import CurrencyService


def create_container() -> punq.Container:
    container = punq.Container()

    container.register(Config)

    engine = create_engine(
        Config.DB_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"connect_timeout": 10}
    )
    container.register("engine", instance=engine)

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    container.register("session_factory", instance=session_factory)

    container.register(
        CurrencyGateway,
        CurrencyHttpGateway,
        base_url=Config.API_BASE_URL,
        timeout=10
    )

    def build_request_repo() -> IRequestRepository:
        session = session_factory()
        return SQLAlchemyRequestRepository(session)

    def build_response_repo() -> IResponseRepository:
        session = session_factory()
        return SQLAlchemyResponseRepository(session)

    container.register(IRequestRepository, factory=build_request_repo)
    container.register(IResponseRepository, factory=build_response_repo)

    container.register(CurrencyService)

    def build_scheduler() -> SchedulerController:
        service = container.resolve(CurrencyService)
        return SchedulerController(
            currency_service=service,
            interval_minutes=Config.REQUEST_INTERVAL_MINUTES
        )

    container.register("SchedulerController", factory=build_scheduler)

    return container

