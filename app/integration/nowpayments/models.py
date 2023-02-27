from pydantic import BaseModel, validator, Field
from datetime import datetime


class PaymentModel(BaseModel):
    payment_id: int
    payment_status: str
    price_amount: float
    price_currency: str
    pay_amount: float
    pay_currency: str
    user_id: int = Field(alias='order_description')
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at', pre=True)
    def parse_datetime(cls, value):
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
