import cv2
import easyocr
import re

reader = easyocr.Reader(['en'])


def detect_plaque(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # amélioration contraste
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    # contours
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(
        edged,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    plaque = None

    for contour in contours:

        approx = cv2.approxPolyDP(
            contour,
            10,
            True
        )

        # plaque = rectangle
        if len(approx) == 4:

            x, y, w, h = cv2.boundingRect(contour)

            ratio = w / h

            # ratio typique plaque
            if ratio > 2:

                plaque = gray[y:y+h, x:x+w]

                break

    if plaque is None:
        return None

    # agrandir image
    plaque = cv2.resize(
        plaque,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # threshold
    plaque = cv2.threshold(
        plaque,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    results = reader.readtext(plaque)

    texte_final = ""

    for result in results:

        texte = result[1]

        texte = texte.upper()

        texte = re.sub(r'[^A-Z0-9 ]', '', texte)

        if len(texte) >= 5:
            texte_final += " " + texte

    return texte_final.strip()