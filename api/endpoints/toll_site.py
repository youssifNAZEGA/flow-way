from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.deps import get_db

from schemas.toll_site import (
    TollSiteCreate,
    TollSiteUpdate
)

from services.toll_site_service import (
    create_toll_site,
    get_all_toll_sites,
    get_active_toll_sites,
    get_toll_site_by_id,
    update_toll_site,
    delete_toll_site
)

router = APIRouter(
    prefix="/toll-sites",
    tags=["Toll Sites"]
)


@router.post("/")
def create_site(
        data: TollSiteCreate,
        db: Session = Depends(get_db)
):

    return create_toll_site(db, data)


@router.get("/")
def get_sites(
        db: Session = Depends(get_db)
):

    return get_all_toll_sites(db)


@router.get("/active")
def get_active_sites(
        db: Session = Depends(get_db)
):

    return get_active_toll_sites(db)


@router.get("/{site_id}")
def get_site(
        site_id: int,
        db: Session = Depends(get_db)
):

    site = get_toll_site_by_id(db, site_id)

    if not site:
        raise HTTPException(
            status_code=404,
            detail="Site introuvable"
        )

    return site


@router.put("/{site_id}")
def update_site(
        site_id: int,
        data: TollSiteUpdate,
        db: Session = Depends(get_db)
):

    site = update_toll_site(
        db,
        site_id,
        data
    )

    if not site:
        raise HTTPException(
            status_code=404,
            detail="Site introuvable"
        )

    return site


@router.delete("/{site_id}")
def delete_site(
        site_id: int,
        db: Session = Depends(get_db)
):

    deleted = delete_toll_site(
        db,
        site_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Site introuvable"
        )

    return {
        "message": "Site supprimé"
    }