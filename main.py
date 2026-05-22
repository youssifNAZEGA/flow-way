from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from db.session import engine
from db.base import Base
from models import *
from api.endpoints.auth import router as auth_router
from api.endpoints.vehicule import router as vehicule_router
from api.endpoints.comptes import router as compte_router
from api.endpoints.passage import router as passage_router
from api.endpoints.passage_history import router as history_router
from api.endpoints.toll_site import router as toll_site_router
from api.endpoints.tariff_config import router as tariff_config_router
from api.endpoints.vehicule_type import router as vehicule_type_router

app = FastAPI()
Base.metadata.create_all(bind = engine)
app.include_router(auth_router)
app.include_router(vehicule_router)
app.include_router(compte_router)
app.include_router(passage_router)
app.include_router(history_router)
app.include_router(toll_site_router)
app.include_router(tariff_config_router)
app.include_router(vehicule_type_router)