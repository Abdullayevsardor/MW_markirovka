from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from pathlib import Path
import os
import shutil
import time
import traceback

from sqlalchemy import text

from app.routers import marking, ui
from app.config import settings
from app.db.session import engine, Base
from app.db import base  # noqa: F401  (modellarni Base'ga ro'yxatdan o'tkazadi)


# /app/app -> /app
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

STATIC_DIR = PROJECT_DIR / "static"                 # Railway'da Volume shu yerga ulanadi
STATIC_CATEGORY = STATIC_DIR / "category"
SOURCE_CATEGORY = PROJECT_DIR / "source_images"     # Volume'dan TASHQARIDA (image ichida)


def wait_for_db(retries: int = 10, delay: float = 3.0) -> None:
    """Railway'da Postgres kechroq ko'tarilishi mumkin — biroz kutamiz."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"[startup] DB ulandi ({attempt}-urinish)")
            return
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"[startup] DB tayyor emas ({attempt}/{retries}): {exc}")
            time.sleep(delay)
    raise RuntimeError(f"DB ga ulanib bo'lmadi: {last_err}")


def seed_category_images() -> None:
    """Volume bo'sh bo'lsa, boshlang'ich kategoriya rasmlarini nusxalaymiz."""
    STATIC_CATEGORY.mkdir(parents=True, exist_ok=True)

    existing = [f for f in STATIC_CATEGORY.iterdir() if f.is_file() and f.name != ".keep"]
    if existing:
        print(f"[startup] static/category'da {len(existing)} ta rasm bor, seed o'tkazib yuborildi")
        return

    if not SOURCE_CATEGORY.exists():
        print(f"[startup] Seed manbasi topilmadi: {SOURCE_CATEGORY}")
        return

    copied = 0
    for src in SOURCE_CATEGORY.iterdir():
        if src.is_file():
            shutil.copy2(src, STATIC_CATEGORY / src.name)
            copied += 1
    print(f"[startup] {copied} ta rasm seed qilindi -> {STATIC_CATEGORY}")


wait_for_db()
Base.metadata.create_all(bind=engine)
seed_category_images()


app = FastAPI(
    title="Maxway Marking System",
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.state.templates = templates
 
STATIC_CATEGORY = "/app/static/category"
SOURCE_CATEGORY = "source_images"

os.makedirs(STATIC_CATEGORY, exist_ok=True)

# print("SOURCE EXISTS:", os.path.exists(SOURCE_CATEGORY))

if len(os.listdir(STATIC_CATEGORY)) <= 1:
    if os.path.exists(SOURCE_CATEGORY):

        for file in os.listdir(SOURCE_CATEGORY):

            src = os.path.join(SOURCE_CATEGORY, file)
            dst = os.path.join(STATIC_CATEGORY, file)

            if os.path.isfile(src):
                shutil.copy2(src, dst)

 


# Routers
app.include_router(ui.router)
app.include_router(marking.router, prefix="/api/marking", tags=["Marking"])


@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(tb)  # Railway loglarida to'liq ko'rinadi
    if settings.is_prod:
        return PlainTextResponse("Internal Server Error", status_code=500)
    return PlainTextResponse(f"Internal Server Error:\n{tb}", status_code=500)
