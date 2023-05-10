from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import MutableMapping
from uvicorn.protocols.utils import get_path_with_query_string
import logging
import time

access_log = logging.getLogger("middleware.access")


def add_middleware(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=access_log_middleware)


def get_client_addr(scope: MutableMapping) -> str:
    """
    Get the host:port client address from the request scope. This function is taken
    from the default access logger in uvicorn, but adds a tuple() cast due to the
    client value being a list in the FastAPI TestClient implementation.
    """
    client = scope.get("client")
    return "%s:%d" % tuple(client) if client else ""


async def access_log_middleware(request: Request, call_next):
    """
    A middleware for generating the route access log. The built-in one for uvicorn
    does not include any information about the response or how long the request took.
    """

    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time

    config = getattr(request.state, "access_log_config", {})

    if not config.get("suppress"):
        access_log.info(
            '%s "%s %s HTTP/%s" %d %.06f',
            get_client_addr(request.scope),
            request.method,
            get_path_with_query_string(request.scope),
            request.scope["http_version"],
            response.status_code,
            process_time,
        )

    return response


def access_log_config(suppress=False):
    """
    A route dependency used to configure access log behavior for any requests made to a
    specific route handler.

        router = APIRouter()

        @router.get("/route/url", dependencies=[Depends(access_log_config(...))])
        def handler():
            ...

    @param suppress (bool):
        Suppress all access log entries for this route.
    """

    def _access_log_config(request: Request):
        request.state.access_log_config = {"suppress": suppress}

    return _access_log_config
