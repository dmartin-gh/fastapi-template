from __future__ import annotations

from sqlalchemy import Column, String, Integer

from fastapi_template.db.models.base import Base


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    col1 = Column(String, unique=True, index=True, nullable=False)
    col2 = Column(Integer)
