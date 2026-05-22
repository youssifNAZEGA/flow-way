from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base import Base
from models import *
from api.endpoints.auth import router as auth_router
from api.endpoints.vehicule import router as vehicule_router
from api.endpoints.comptes import router as compte_router
from api.endpoints.passages import router as passage_router
from api.endpoints.toll_site import router as toll_site_router
from api.endpoints.tariff_config import router as tariff_config_router
from api.endpoints.vehicule_type import router as vehicule_type_router
from api.endpoints.notifications import router as notification_router
from api.endpoints.admin import router as admin_router
from api.endpoints.manager import router as manager_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind = engine)

# API V1
api_v1_prefix = "/api/v1"

app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(vehicule_router, prefix=api_v1_prefix)
app.include_router(compte_router, prefix=api_v1_prefix)
app.include_router(passage_router, prefix=api_v1_prefix)
app.include_router(toll_site_router, prefix=api_v1_prefix)
app.include_router(tariff_config_router, prefix=api_v1_prefix)
app.include_router(vehicule_type_router, prefix=api_v1_prefix)
app.include_router(notification_router, prefix=api_v1_prefix)
app.include_router(admin_router, prefix=api_v1_prefix)
app.include_router(manager_router, prefix=api_v1_prefix)
