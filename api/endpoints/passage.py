from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from db.deps import get_db
from services.passage_service import process_passage
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

    # OCR
    plaque = detect_plaque(image_path)

    if not plaque:
        return {
            "success": False,
            "message": "Plaque non trouvée"
        }

    result = process_passage(db=db, plaque=plaque)

    return {
        "success": True,
        "plaque": plaque,
        "result": result
    }