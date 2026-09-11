# 🔐 MARKIROKA LOYIHASI - MA'LUMOT BACKUP

**Saqlanish sanasi:** 2026-09-11 17:39 UTC+5
**Loyiha:** Markiroka (MW_markirovka)
**Repository:** Abdullayevsardor/MW_markirovka

---

## 📋 MUHIM ENVIRONMENT VARIABLES

```
ENV=prod
DOMAIN=example.com
LETSENCRYPT_EMAIL=admin@example.com

# Database Configuration
DB_USER=marking_user
DB_PASSWORD=sardor1432
DB_NAME=marking_db
DB_HOST=db
DB_PORT=5432

# Application Secrets (CURRENT VALUES)
SECRET_KEY=CHANGE_ME_SUPER_SECRET
ADMIN_PASSWORD=CHANGE_ME_ADMIN_PASS
```

---

## 🗄️ DATABASE STRUCTURE

- **Type:** PostgreSQL 18
- **Database Name:** marking_db
- **Database User:** marking_user
- **Password:** sardor1432
- **Port:** 5432

### Models (Tables):
1. **User** - Foydalanuvchilar
2. **Category** - Kategoriyalar
3. **Products** - Mahsulotlar
4. **Marking** - Belgilash/Imlosi

**Migration Tool:** Alembic

---

## 🔧 ASOSIY KOMPONENTLAR

- **Framework:** FastAPI (Python)
- **Web Server:** Uvicorn
- **Database:** PostgreSQL 18
- **Cache/Queue:** Redis 7
- **Async Worker:** Celery

---

## ✅ LOYIHANI YANGI BOSHTAN QURISH UCHUN:

1. SECRET_KEY va ADMIN_PASSWORD environment variables'ni qo'shing
2. PostgreSQL database'ni Railway'da yarating yoki DATABASE_URL qo'shing
3. Redis'ni qo'shing (Celery uchun)
4. Qayta deploy qiling

Barcha ma'lumot butha faylda saqlanib qoldi!
