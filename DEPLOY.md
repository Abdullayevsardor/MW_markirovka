# Railway'ga deploy qilish

Loyiha: FastAPI + PostgreSQL. Redis/Celery **ishlatilmaydi** (kod bor, lekin hech qayerda
chaqirilmaydi) — shuning uchun Railway'da ular uchun alohida service ochilmaydi.

---

## 1. Kodni GitHub'ga yuklash

```bash
git add -A
git commit -m "Railway deploy uchun tayyorlash"
git push origin main
```

## 2. Railway'da loyiha yaratish

1. https://railway.app → **New Project** → **Deploy from GitHub repo**
2. `Abdullayevsardor/MW_markirovka-main` reposini tanlang
3. Railway `railway.json`ni ko'rib, `Dockerfile` bilan build qiladi

## 3. Postgres qo'shish

Loyiha ichida: **+ New** → **Database** → **Add PostgreSQL**

## 4. Environment variables (web service → Variables)

| Nomi | Qiymati |
|---|---|
| `DATABASE_URL` | `${{ Postgres.DATABASE_URL }}` ← shu ko'rinishda, Railway o'zi almashtiradi |
| `SECRET_KEY` | uzun tasodifiy satr |
| `ADMIN_PASSWORD` | admin panel paroli |
| `ENV` | `prod` |
| `TZ` | `Asia/Tashkent` |

`SECRET_KEY` yaratish:
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

> `DB_USER`, `DB_PASSWORD` va h.k. Railway'da **kerak emas** — `DATABASE_URL` ustun turadi.

## 5. Volume (yuklangan rasmlar yo'qolmasligi uchun)

Web service → **Settings** → **Volumes** → **Add Volume**

- **Mount path:** `/app/static/category`

> ⚠️ `/app/static` EMAS, aynan `/app/static/category`.
> Aks holda `/static/logo/logo.png` image ichidan yo'qoladi va sayt logosi ko'rinmay qoladi.

Volume birinchi marta bo'sh bo'ladi — ilova ishga tushganda `source_images/` dagi 5 ta
boshlang'ich rasmni avtomatik nusxalaydi (`seed_category_images()` in `app/main.py`).

## 6. Domen

Web service → **Settings** → **Networking** → **Generate Domain**

`https://<nom>.up.railway.app` — HTTPS avtomatik, sertifikat kerak emas.

## 7. Tekshirish

| URL | Nima bo'lishi kerak |
|---|---|
| `/healthz` | `{"status":"ok"}` |
| `/` | Kategoriyalar sahifasi + logo |
| `/admin-login` | Parol so'raydi (`ADMIN_PASSWORD`) |

Loglar: Railway → service → **Deployments** → **View Logs**.
Ishga tushganda ko'rinadi:
```
[startup] DB ulandi (1-urinish)
[startup] 5 ta rasm seed qilindi -> /app/static/category
```

---

## Lokal ishga tushirish (docker-compose)

```bash
cp .env.example .env      # ichidagi parollarni o'zgartiring
docker compose up --build
```
→ http://localhost:8000

---

## Keyinchalik: xavfsizlik (deploy'dan keyin hal qilish kerak)

1. **Admin himoyasi zaif.** `/admin?token=ok` — URL'ni bilgan har kim admin panelga kiradi.
   Session cookie yoki JWT'ga o'tkazish kerak.
2. **Alembic buzuq** (`alembic/env.py` da `settings.config` mavjud emas, `versions/` bo'sh).
   Hozir jadvallar `Base.metadata.create_all()` bilan yaratiladi — yangi ustun qo'shilsa,
   mavjud jadvalga avtomatik qo'shilmaydi. Migratsiya kerak bo'lganda Alembic'ni tuzatish lozim.
3. `app/static/` papkasi ishlatilmaydi (`/static` ildizdagi `static/` dan xizmat qiladi).
