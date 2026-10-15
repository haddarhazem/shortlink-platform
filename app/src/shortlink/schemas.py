import datetime as dt

from pydantic import AnyHttpUrl, BaseModel, field_validator


class LinkCreate(BaseModel):
    target_url: AnyHttpUrl

    @field_validator("target_url")
    @classmethod
    def _max_length(cls, v: AnyHttpUrl) -> AnyHttpUrl:
        if len(str(v)) > 2048:
            raise ValueError("URL is too long (max 2048 characters)")
        return v


class LinkOut(BaseModel):
    code: str
    short_url: str
    target_url: str


class DailyClicks(BaseModel):
    date: dt.date
    clicks: int


class LinkStats(BaseModel):
    code: str
    target_url: str
    total_clicks: int
    daily: list[DailyClicks]
