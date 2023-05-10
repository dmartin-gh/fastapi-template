from fastapi import FastAPI

from . import health
from . import example


def add_routers(app: FastAPI):
    app.include_router(health.router)
    app.include_router(example.router)
