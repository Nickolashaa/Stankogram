from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class HealthResponse(Schema):
    code: int
    message: str
