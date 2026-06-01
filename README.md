# BD Kutná Hora – Strakoschova

Webový portál Bytového družstva Kutná Hora Strakoschova.

## Technologie

- **Django 5.2** + **PostgreSQL 16** (backend)
- **Docker Compose** (kontejnerizace)
- **Tailwind CSS** přes CDN (frontend)
- **Whitenoise** (statické soubory)

## Požadavky

- **Docker** + **Docker Compose** – jediné co potřebuješ pro spuštění aplikace

## Rychlý start

```bash
# 1. Zkopíruj prostředí
cp .env.example .env

# 2. Spusť aplikaci
docker compose up --build
```

Aplikace bude dostupná na **http://localhost:8000**

Admin rozhraní: **http://localhost:8000/admin/**

## Stránky

| URL               | Popis                                              |
|-------------------|----------------------------------------------------|
| `/`               | Úvodní strana                                      |
| `/nastenka/`      | Digitální nástěnka (oznámení, schůze, dokumenty)  |
| `/kontakty/`      | Kontakty a havarijní služba                        |
| `/zakladni-info/` | Základní informace o družstvu                      |
| `/admin/`         | Administrace (správa příspěvků)                    |

## Užitečné příkazy

```bash
# Spustit migrace
docker compose exec web python manage.py migrate

# Vytvořit administrátorský účet
docker compose exec web python manage.py createsuperuser

# Importovat ukázkové příspěvky z posts.json
docker compose exec web python manage.py import_posts

# Zastavit kontejnery
docker compose down

# Zastavit a smazat data (databáze, média)
docker compose down -v
```

## Testy

**V Dockeru** (doporučeno – používá PostgreSQL stejně jako produkce):

```bash
docker compose exec web python manage.py test
```

**Lokálně bez Dockeru** (používá SQLite):

```bash
pip install -r requirements.txt
python manage.py test --settings=bd_project.test_settings
```

## Produkční nasazení

Pro produkci uprav `.env`:

```env
DEBUG=False
SECRET_KEY=<silný-náhodný-klíč>
DATABASE_URL=postgres://user:pass@host:5432/dbname
ALLOWED_HOSTS=tvaradomena.cz,www.tvaradomena.cz
```
