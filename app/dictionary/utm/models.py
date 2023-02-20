from pydantic import BaseModel, Field


class NewTrafficSource(BaseModel):
    source: str = Field(alias='utm_source')
    medium: str = Field(alias='utm_medium')
    campaign: str = Field(alias='utm_campaign')
    content: int = Field(alias='utm_content')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
