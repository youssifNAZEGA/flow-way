# from dotenv import load_dotenv
# load_dotenv()

# from fastapi import FastAPI
# from db.session import engine
# from db.base import Base
# from models import *
# from api.endpoints.auth import router as auth_router
# from api.endpoints.vehicule import router as vehicule_router
# from api.endpoints.comptes import router as compte_router
# from api.endpoints.passage import router as passage_router



# app = FastAPI()
# Base.metadata.create_all(bind = engine)
# app.include_router(auth_router)
# app.include_router(vehicule_router)
# app.include_router(compte_router)
# app.include_router(passage_router)




# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routeurs existants
from api.endpoints.auth import router as auth_router
from api.endpoints.passage import router as passage_router
from api.endpoints.comptes import router as comptes_router
from api.endpoints.vehicule import router as vehicule_router

# 👇 Nouveaux routeurs à ajouter
from api.endpoints.notification import router as notification_router
from api.endpoints.supervision import router as supervision_router

app = FastAPI(
    title="SMART PÉAGE - FlowWay",
    description="API de gestion de péage automatisé (Reconnaissance plaque + Portefeuille)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS (optionnel mais recommandé pour le frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace par tes domaines en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 Enregistrement des routeurs
app.include_router(auth_router)
app.include_router(comptes_router)
app.include_router(vehicule_router)
app.include_router(passage_router)
app.include_router(notification_router)   # ✅ Apparaîtra sous /notifications
app.include_router(supervision_router)    # ✅ Apparaîtra sous /supervision

@app.get("/")
def root():
    return {"message": "SMART PÉAGE API is running 🚀", "docs": "/docs"}
