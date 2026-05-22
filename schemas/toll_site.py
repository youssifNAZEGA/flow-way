from pydantic import BaseModel


class TollSiteCreate(BaseModel):
    name: str
    address: str
    latitude: str
    longitude: str
    lanes_count: int


class TollSiteUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    lanes_count: int | None = None
    is_active: bool | None = None


class TollSiteResponse(BaseModel):
    id: int
    name: str
    address: str
    latitude: str
    longitude: str
    is_active: bool
    lanes_count: int

    class Config:
        from_attributes = True