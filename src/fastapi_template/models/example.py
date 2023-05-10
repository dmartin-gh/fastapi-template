from pydantic import BaseModel


class ExampleBase(BaseModel):
    pass


class ExampleResponse(ExampleBase):
    id: int
    col1: str
    col2: int

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
