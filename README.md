# Coderr Backend

REST API für die Coderr-Plattform – eine Freelance-Marketplace-App, auf der Business-User Angebote erstellen und Customer-User diese buchen und bewerten können.

**Stack:** Django 6 · Django REST Framework · SQLite · Token Authentication

---

## Voraussetzungen

- Python 3.11+
- pip

---

## Installation

### 1. Repository klonen

```bash
git clone <repository-url>
cd Coderr-Backend
```

### 2. Virtuelle Umgebung erstellen und aktivieren

**Mac / Linux**
```bash
python3 -m venv env
source env/bin/activate
```

**Windows**
```bash
python -m venv env
env\Scripts\activate
```

### 3. Abhängigkeiten installieren

**Mac / Linux**
```bash
pip3 install -r requirements.txt
```

**Windows**
```bash
pip install -r requirements.txt
```

### 4. Datenbank migrieren

**Mac / Linux**
```bash
python3 manage.py migrate
```

**Windows**
```bash
python manage.py migrate
```

### 5. (Optional) Superuser erstellen

**Mac / Linux**
```bash
python3 manage.py createsuperuser
```

**Windows**
```bash
python manage.py createsuperuser
```

### 6. Entwicklungsserver starten

**Mac / Linux**
```bash
python3 manage.py runserver
```

**Windows**
```bash
python manage.py runserver
```

Die API ist anschließend unter `http://127.0.0.1:8000/` erreichbar.

---

## Projektstruktur

```
Coderr-Backend/
├── core/               # Django-Projektkonfiguration (settings, urls)
├── users_app/          # Registrierung, Login, Benutzerprofile
├── offers_app/         # Angebote und Angebotsdetails
├── orders_app/         # Bestellungen
├── reviews_app/        # Bewertungen
├── requirements.txt
└── manage.py
```

---

## API-Übersicht

Alle Endpunkte sind unter `/api/` erreichbar. Eine vollständige Dokumentation befindet sich in [api_endpoints.md](api_endpoints.md).

| Bereich       | Endpunkt                                      | Methoden          |
|---------------|-----------------------------------------------|-------------------|
| Auth          | `/api/registration/`                          | POST              |
| Auth          | `/api/login/`                                 | POST              |
| Profile       | `/api/profile/<id>/`                          | GET, PATCH        |
| Profile       | `/api/profiles/business/`                     | GET               |
| Profile       | `/api/profiles/customer/`                     | GET               |
| Offers        | `/api/offers/`                                | GET, POST         |
| Offers        | `/api/offers/<id>/`                           | GET, PATCH, DELETE|
| Offers        | `/api/offerdetails/<id>/`                     | GET               |
| Orders        | `/api/orders/`                                | GET, POST         |
| Orders        | `/api/orders/<id>/`                           | PATCH, DELETE     |
| Orders        | `/api/order-count/<business_user_id>/`        | GET               |
| Orders        | `/api/completed-order-count/<business_user_id>/` | GET            |
| Reviews       | `/api/reviews/`                               | GET, POST         |
| Reviews       | `/api/reviews/<id>/`                          | PATCH, DELETE     |
| Stats         | `/api/base-info/`                             | GET               |

### Authentifizierung

Alle Endpunkte (außer `/api/registration/`, `/api/login/`, `/api/offers/` GET und `/api/base-info/`) erfordern einen Token im Header:

```
Authorization: Token <dein-token>
```

---

## Admin-Panel

Das Django-Adminpanel ist unter `http://127.0.0.1:8000/admin/` erreichbar (Superuser erforderlich).
