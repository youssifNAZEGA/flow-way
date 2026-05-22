from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.deps import get_db
from db.security import get_current_user, require_manager_role
from services.supervision_service import (
    get_realtime_passages, 
    get_dashboard_stats, 
    manually_validate_passage
)
from schemas.supervision import PassageBrief, SupervisionStats
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/supervision", tags=["Supervision Gestionnaire"])

@router.get("/passages/realtime", response_model=List[PassageBrief])
def view_realtime_passages(
    site_id: Optional[int] = Query(None, description="Filtrer par site de péage"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_role)
):
    """BF-054: Supervision des passages en temps réel"""
    return get_realtime_passages(db, site_id, limit)

@router.get("/dashboard/stats", response_model=SupervisionStats)
def view_dashboard_stats(
    site_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_role)
):
    """Statistiques du tableau de bord de supervision"""
    return get_dashboard_stats(db, site_id)

@router.post("/passages/{passage_id}/validate", response_model=PassageBrief)
def manual_validation(
    passage_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager_role)
):
    """BF-036: Validation manuelle d'un passage (en cas d'échec LPR)"""
    try:
        return manually_validate_passage(db, passage_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))