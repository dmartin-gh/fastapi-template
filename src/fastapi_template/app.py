from fastapi import FastAPI
from contextlib import asynccontextmanager
from importlib.metadata import version
import os

from .settings import Settings
from .db.manager import DatabaseManager
from .middleware import add_middleware
from .routes import add_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.api.state.settings
    async with DatabaseManager(settings.SQLALCHEMY_DATABASE_URI) as db:
        app.state.api.state.db = db
        yield


def create_app() -> FastAPI:
    api = FastAPI(
        title="FastAPI Template Service",
        version=version("fastapi-template"),
        openapi_url="/swagger.json",
        docs_url="/swagger",
    )

    api.state.settings = Settings()

    add_middleware(api)
    add_routers(api)

    app = FastAPI(lifespan=lifespan)
    app.mount("/api/fastapi-template", api)
    app.state.api = api

    return app
