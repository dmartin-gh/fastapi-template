from fastapi import APIRouter, Depends

from fastapi_template.services.example import ExampleService
from fastapi_template.db.models import Example
from fastapi_template.models.example import ExampleResponse

router = APIRouter()


@router.get("/example", response_model=list[ExampleResponse])
async def get_example_data(
    service: ExampleService = Depends(ExampleService),
) -> list[Example]:
    return await service.get_example_data()
