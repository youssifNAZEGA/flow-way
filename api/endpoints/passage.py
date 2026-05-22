# from fastapi import APIRouter, UploadFile, File, Depends
# from sqlalchemy.orm import Session
# from db.deps import get_db
# from services.passage_service import process_passage
# from utils.ocr import detect_plaque

# router = APIRouter(prefix="/passage", tags=["Passage"])


# @router.post("/image")
# async def process_image(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     contents = await file.read()

#     image_path = "temp.jpg"

#     with open(image_path, "wb") as f:
#         f.write(contents)

#     # OCR
#     plaque = detect_plaque(image_path)

#     if not plaque:
#         return {
#             "success": False,
#             "message": "Plaque non trouvée"
#         }

#     result = process_passage(db=db, plaque=plaque)

#     return {
#         "success": True,
#         "plaque": plaque,
#         "result": result
#     }



from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from db.deps import get_db
from services.passage_service import process_passage
from services.notification_service import (
    notify_passage_success,
    notify_low_balance,
    notify_negative_balance,
    notify_credit_used,
    notify_account_blocked
)
from utils.ocr import detect_plaque

router = APIRouter(prefix="/passage", tags=["Passage"])

@router.post("/image")
async def process_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    image_path = "temp.jpg"
    
    with open(image_path, "wb") as f:
        f.write(contents)

    # OCR - Détection plaque
    plaque = detect_plaque(image_path)
    if not plaque:
        return {"success": False, "message": "Plaque non trouvée"}

    # Traitement du passage
    result = process_passage(db=db, plaque=plaque)
    
    # result doit contenir: 
    # - user_id
    # - montant
    # - site_nom
    # - nouveau_solde
    # - credits_utilises
    # - statut (reussi, credit_utilise, bloque)

    # 📩 Notifications selon le scénario (BF-041 à BF-047)
    if result["statut"] == "reussi":
        notify_passage_success(
            db, 
            result["user_id"], 
            plaque, 
            result["montant"], 
            result["site_nom"]
        )
        notify_low_balance(db, result["user_id"], result["nouveau_solde"])
    
    elif result["statut"] == "credit_utilise":
        notify_credit_used(db, result["user_id"], result["credits_restants"])
        notify_negative_balance(
            db, 
            result["user_id"], 
            result["nouveau_solde"], 
            result["credits_utilises"]
        )
    
    elif result["statut"] == "bloque":
        notify_account_blocked(db, result["user_id"])

    return {
        "success": True,
        "plaque": plaque,
        "result": result
    }