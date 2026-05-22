from pydantic import BaseModel


class VehicleTypeCreate(BaseModel):
    name: str
    description: str | None = None


class TariffConfigCreate(BaseModel):
    vehicle_type_id: int
    toll_site_id: int
    amount: int


class TariffConfigUpdate(BaseModel):
    amount: int | None = None
    is_active: bool | None = None