from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from fastapi_template.middleware import access_log_config

router = APIRouter()


@router.get(
    "/health",
    response_class=PlainTextResponse,
    dependencies=[Depends(access_log_config(suppress=True))],
)
async def health():
    """
    Return the health status of this service as an HTTP response code. If the
    service is healthy, a '200 OK' response is sent with the text "success".
    """
    return "success"
