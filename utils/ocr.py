import cv2
import easyocr
import re

reader = easyocr.Reader(['en'])

def detect_plaque(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    # Agrandir image
    image = cv2.resize(image, None, fx=2, fy=2)

    # Gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Réduction bruit
    blur = cv2.bilateralFilter(gray, 11, 17, 17)

    # Contraste
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # OCR
    results = reader.readtext(thresh)

    textes = []

    for res in results:
        text = res[1]

        # Nettoyage
        text = text.upper()
        text = re.sub(r'[^A-Z0-9 ]', '', text)

        textes.append(text)

    texte_final = " ".join(textes)

    print("OCR:", texte_final)

    # Recherche format plaque
    match = re.search(r'(TG)?\s?(\d{3,4})\s?([A-Z]{1,3})', texte_final)

    if match:
        numero = match.group(2)
        lettres = match.group(3)

        return f"TG {numero} {lettres}"

    return None