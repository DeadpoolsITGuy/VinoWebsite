from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Header
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import secrets
import uuid
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'vino2025')

# Simple in-memory token store (fine for a single-admin MVP)
ACTIVE_TOKENS = set()

# Create the main app
app = FastAPI()

api_router = APIRouter(prefix="/api")


# ---------- Models ----------
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StatusCheckCreate(BaseModel):
    client_name: str


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    token: str


class WineItem(BaseModel):
    name: str
    price: str


class MenuData(BaseModel):
    fizz: List[WineItem] = []
    white: List[WineItem] = []
    orange: List[WineItem] = []
    rose: List[WineItem] = []
    red: List[WineItem] = []


class SiteConfig(BaseModel):
    hero_image_url: Optional[str] = None
    hero_images: Optional[List[str]] = None
    hero_tagline: Optional[str] = None
    since_year: Optional[str] = "MMXXV"
    rotate_seconds: Optional[int] = 6


# ---------- Defaults ----------
DEFAULT_MENU: Dict[str, List[Dict[str, str]]] = {
    "fizz": [
        {"name": "Prosecco Extra Dry, Canal Grando, Italy", "price": "28 / 5.5"},
        {"name": "Crémant de Bourgogne Brut, France", "price": "36 / 6.5"},
        {"name": "Cava Brut, + & + Seleccion, Spain", "price": "31"},
        {"name": "Lambrusco Rosso Secco La Favorita, Italy", "price": "26"},
        {"name": "Franciacorta Extra Brut, Italy", "price": "60"},
    ],
    "white": [
        {"name": "Blanc de Blanc, Château Oumsiyat, Lebanon", "price": "26 / 6.5"},
        {"name": "Picpoul de Pinet, Le Montalus, France", "price": "29 / 7"},
        {"name": "Fernão Pires, Cintila, Portugal", "price": "24 / 6"},
        {"name": "Sauvignon Blanc, Lomond Wines, South Africa", "price": "34 / 8.5"},
        {"name": "Verdeca, Talò, San Marzano, Italy", "price": "29 / 7.5"},
        {"name": "Gavi Villa Sparina, Italy", "price": "35"},
        {"name": "Zibibbo, Vitese, Colomba Bianca, Italy", "price": "28"},
        {"name": "Grenache Blanc, Big Buzz, France", "price": "27"},
        {"name": "Viognier, No es Pituko, Chile", "price": "35"},
    ],
    "orange": [
        {"name": "Orange, No es Pituko, Chile", "price": "32 / 8"},
    ],
    "rose": [
        {"name": "Castelão Rosé, Cintila, Portugal", "price": "24 / 6"},
        {"name": "Rosato, Anemone, Alghero, Italy", "price": "29 / 7"},
        {"name": "Syrah/Grenache Rosé, Le Campuget, France", "price": "27"},
    ],
    "red": [
        {"name": "Rioja Alavesa, Mayela, Bideona, Spain", "price": "29 / 7.5"},
        {"name": "Castelão, Cintila, Portugal", "price": "24 / 6"},
        {"name": "Montepulciano Blend, Anima Osca, Italy", "price": "32 / 8"},
        {"name": "Malbec, Terroir Unico, Argentina", "price": "34 / 9"},
        {"name": "Mucchietto, Italy", "price": "34"},
        {"name": "Chianti, Gentilesco, Bonacchi, Italy", "price": "28"},
        {"name": "Barbera d’Alba, Terre del Barolo, Italy", "price": "32"},
        {"name": "Pinot Noir, Little Yering, Australia", "price": "35"},
        {"name": "Saperavi, Vachnadziani Winery, Georgia", "price": "27"},
        {"name": "Cabernet Sauvignon, No es Pituko, Chile", "price": "30"},
        {"name": "Amarone, Italy", "price": "50"},
    ],
}

DEFAULT_SITE_CONFIG = {
    "hero_image_url": "https://images.squarespace-cdn.com/content/v1/67f667faca6fd714aaa732b0/dcb76f8f-f576-4f2a-a31d-031d8d8a7698/uliana-kopanytsia-epHhP3H71sw-unsplash.jpg",
    "hero_images": [
        "https://images.squarespace-cdn.com/content/v1/67f667faca6fd714aaa732b0/dcb76f8f-f576-4f2a-a31d-031d8d8a7698/uliana-kopanytsia-epHhP3H71sw-unsplash.jpg",
    ],
    "hero_tagline": "by tonino",
    "since_year": "MMXXV",
    "rotate_seconds": 6,
}


# ---------- Auth dep ----------
def require_admin(authorization: Optional[str] = Header(None)) -> bool:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    if token not in ACTIVE_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


# ---------- Public routes ----------
@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.dict())
    await db.status_checks.insert_one(status_obj.dict())
    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**s) for s in status_checks]


@api_router.get("/menu")
async def get_menu():
    doc = await db.menu.find_one({"_id": "current"})
    if not doc:
        return DEFAULT_MENU
    doc.pop("_id", None)
    return doc


@api_router.get("/site-config")
async def get_site_config():
    doc = await db.site_config.find_one({"_id": "current"})
    if not doc:
        return DEFAULT_SITE_CONFIG
    doc.pop("_id", None)
    # Normalise: ensure hero_images is populated, fall back to hero_image_url
    if not doc.get("hero_images"):
        if doc.get("hero_image_url"):
            doc["hero_images"] = [doc["hero_image_url"]]
        else:
            doc["hero_images"] = DEFAULT_SITE_CONFIG["hero_images"]
    if not doc.get("hero_image_url") and doc.get("hero_images"):
        doc["hero_image_url"] = doc["hero_images"][0]
    return doc


# ---------- Admin routes ----------
@api_router.post("/admin/login", response_model=LoginResponse)
async def admin_login(payload: LoginRequest):
    if payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = secrets.token_urlsafe(32)
    ACTIVE_TOKENS.add(token)
    return {"token": token}


@api_router.get("/admin/verify")
async def admin_verify(_: bool = Depends(require_admin)):
    return {"ok": True}


@api_router.put("/admin/menu")
async def update_menu(menu: MenuData, _: bool = Depends(require_admin)):
    data = menu.dict()
    await db.menu.update_one(
        {"_id": "current"},
        {"$set": data},
        upsert=True,
    )
    return data


@api_router.put("/admin/site-config")
async def update_site_config(cfg: SiteConfig, _: bool = Depends(require_admin)):
    data = {k: v for k, v in cfg.dict().items() if v is not None}
    await db.site_config.update_one(
        {"_id": "current"},
        {"$set": data},
        upsert=True,
    )
    doc = await db.site_config.find_one({"_id": "current"})
    doc.pop("_id", None)
    return doc


@api_router.post("/admin/upload")
async def upload_image(file: UploadFile = File(...), _: bool = Depends(require_admin)):
    allowed = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Only jpg/png/webp images allowed")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File larger than 10MB")
    image_id = uuid.uuid4().hex
    await db.images.insert_one({
        "_id": image_id,
        "content_type": file.content_type,
        "data": content,
        "filename": file.filename or f"{image_id}.jpg",
        "created_at": datetime.utcnow(),
    })
    return {"url": f"/api/images/{image_id}", "filename": file.filename or image_id}


@api_router.get("/images/{image_id}")
async def get_image(image_id: str):
    doc = await db.images.find_one({"_id": image_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(
        content=doc["data"],
        media_type=doc.get("content_type", "image/jpeg"),
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@api_router.delete("/admin/images/{image_id}")
async def delete_image(image_id: str, _: bool = Depends(require_admin)):
    res = await db.images.delete_one({"_id": image_id})
    return {"deleted": res.deleted_count > 0}


# ---------- Wire up ----------
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
