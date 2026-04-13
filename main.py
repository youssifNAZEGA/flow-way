from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from db.session import engine
from db.base import Base
from models import *
from api.endpoints.auth import router as auth_router
from api.endpoints.vehicule import router as vehicule_router
from api.endpoints.comptes import router as compte_router




app = FastAPI()
Base.metadata.create_all(bind = engine)
app.include_router(auth_router)
app.include_router(vehicule_router)
app.include_router(compte_router)
