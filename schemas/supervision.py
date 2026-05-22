from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PassageBrief(BaseModel):
    id: int
    plaque: Optional[str] = None
    site_nom: Optional[str] = None
    date_heure: datetime
    montant: float
    statut: str
    image_plaque_url: Optional[str] = None
    valide_par: Optional[int] = None

    model_config = {"from_attributes": True}

class SupervisionStats(BaseModel):
    total_passages_today: int
    success_count: int
    manual_validation_count: int
    lpr_success_rate: float

    model_config = {"from_attributes": True}