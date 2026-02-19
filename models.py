from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    endpoint = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    responses = relationship(
        "Response",
        back_populates="request",
        cascade="all, delete-orphan"
    )



class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False, index=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    rate = Column(Numeric(15, 6), nullable=False)
    date = Column(String(10), nullable=False)
    raw_data = Column(Text, nullable=False)

    request = relationship("Request", back_populates="responses")

