from datetime import datetime
from pydantic import BaseModel, Field, validator
import json


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


class ReportInside(BaseModel):
    rating: list
    urls: dict
    partners: dict
    utmStat: dict
    usersMeta: dict


class ReportInsideModel(BaseModel):
    _id: str
    group: str
    roomid: str
    webinarId: str
    playFromRoom: str
    report: ReportInside
    messages: dict
    messagesTS: dict
    ver: int
    created: datetime

    @validator('report', 'messages', 'messagesTS', pre=True)
    def convert_json(cls, value):
        return json.loads(value)

    @validator('created', pre=True)
    def parse_datetime(cls, value):
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')


class WebinarData(BaseModel):
    report: ReportInsideModel
    room_title: str
    customFields: dict
