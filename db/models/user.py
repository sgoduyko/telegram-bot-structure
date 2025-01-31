from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(15), nullable=False, unique=True)
    pincode: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
