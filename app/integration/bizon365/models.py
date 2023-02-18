from datetime import datetime
from pydantic import BaseModel, Field, validator


class WebinarRoomModel(BaseModel):
    id: str
    title: str
    is_autowebinar: bool = Field(alias="isAutowebinar")
    closest_date: bool | datetime = Field(alias="closestDate")

    @validator("closest_date", pre=True, each_item=False)
    def closest_date_convert(cls, value):
        return None if isinstance(value, bool) else value

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

