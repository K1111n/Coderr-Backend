# Coderr Backend

REST API for the Coderr platform – a freelance marketplace where business users can create offers and customers can book and review them.

**Stack:** Django 6 · Django REST Framework · SQLite · Token Authentication

---

## Prerequisites

- Python 3.11+
- pip

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Coderr-Backend
```

### 2. Create and activate a virtual environment

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

### 3. Install dependencies

**Mac / Linux**
```bash
pip3 install -r requirements.txt
```

**Windows**
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

**Mac / Linux**
```bash
cp .env.example .env
```

**Windows**
```bash
copy .env.example .env
```

Then fill in the `.env` file with your own `SECRET_KEY`.

### 5. Run database migrations

**Mac / Linux**
```bash
python3 manage.py migrate
```

**Windows**
```bash
python manage.py migrate
```

### 6. (Optional) Create a superuser

**Mac / Linux**
```bash
python3 manage.py createsuperuser
```

**Windows**
```bash
python manage.py createsuperuser
```

### 7. Start the development server

**Mac / Linux**
```bash
python3 manage.py runserver
```

**Windows**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## Project Structure

```
Coderr-Backend/
├── core/               # Django project configuration (settings, urls)
├── users_app/          # Registration, login, user profiles
├── offers_app/         # Offers and offer details
├── orders_app/         # Orders
├── reviews_app/        # Reviews
├── requirements.txt
└── manage.py
```

---

## API Overview

All endpoints are available under `/api/`. Full documentation can be found in [api_endpoints.md](api_endpoints.md).

| Section       | Endpoint                                         | Methods           |
|---------------|--------------------------------------------------|-------------------|
| Auth          | `/api/registration/`                             | POST              |
| Auth          | `/api/login/`                                    | POST              |
| Profile       | `/api/profile/<id>/`                             | GET, PATCH        |
| Profile       | `/api/profiles/business/`                        | GET               |
| Profile       | `/api/profiles/customer/`                        | GET               |
| Offers        | `/api/offers/`                                   | GET, POST         |
| Offers        | `/api/offers/<id>/`                              | GET, PATCH, DELETE|
| Offers        | `/api/offerdetails/<id>/`                        | GET               |
| Orders        | `/api/orders/`                                   | GET, POST         |
| Orders        | `/api/orders/<id>/`                              | PATCH, DELETE     |
| Orders        | `/api/order-count/<business_user_id>/`           | GET               |
| Orders        | `/api/completed-order-count/<business_user_id>/` | GET               |
| Reviews       | `/api/reviews/`                                  | GET, POST         |
| Reviews       | `/api/reviews/<id>/`                             | PATCH, DELETE     |
| Stats         | `/api/base-info/`                                | GET               |

### Authentication

All endpoints (except `/api/registration/`, `/api/login/`, `GET /api/offers/` and `/api/base-info/`) require a token in the request header:

```
Authorization: Token <your-token>
```

---

## Admin Panel

The Django admin panel is available at `http://127.0.0.1:8000/admin/` (superuser required).
