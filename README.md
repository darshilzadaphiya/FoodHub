# FoodHub 🍔

> A full-stack food item management web application built with Django, featuring user authentication, REST API endpoints, soft-delete functionality, custom middleware, and PostgreSQL — deployed on Railway.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.3-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.17-A30000?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css&logoColor=white)
![Deployed](https://img.shields.io/badge/Deployed-Railway-0B0D0E?logo=railway&logoColor=white)

🌐 **Live Demo:** [foodhub-production.up.railway.app](https://foodhub-production.up.railway.app)

---

## 📖 Overview

FoodHub is a Django-based web application that lets authenticated users create, browse, update, and delete food items in a shared catalogue. Each user owns the items they post, and only the owner can edit or delete their own entries. The project was built as a learning exercise to demonstrate end-to-end Django proficiency — from ORM modelling and authentication to custom middleware, REST APIs, and production deployment.

---

## ✨ Features

### Core Functionality
- 🔐 **User authentication** — registration, login, logout, and profile pages
- 🍽️ **Food item CRUD** — create, view, update, and (soft-)delete menu items
- 🖼️ **Image support** — each item carries an image URL with a sensible fallback
- 👤 **Ownership control** — users can only edit or delete their own items
- 📄 **Pagination** — 5 items per page on the catalogue view
- 💰 **Custom template filters** — currency formatting via `{{ price|currency }}`

### Backend Engineering
- ♻️ **Soft delete pattern** — items are marked `is_deleted=True` rather than removed; recoverable via the `all_objects` manager
- 🧩 **Custom model manager** — `ItemManager` automatically hides deleted items from default queries
- 🚦 **Custom middleware** — request logging, response-time tracking, and IP blocking
- 📊 **Database indexing** — composite index on `(user_name, item_price)` plus individual indexes on `item_name` and `item_price` for query performance
- 📝 **Structured logging** — file and console handlers configured in `settings.py`
- ⚡ **File-based caching** — wired up via Django's caching framework

### REST API (Django REST Framework)
- `GET /myapp/item-json/` — returns all items as JSON using `ItemSerializer`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0.3, Django REST Framework 3.17.1 |
| **Database** | PostgreSQL (via `psycopg` 3.3) |
| **Frontend** | Django Templates + Tailwind CSS (CDN) |
| **Auth** | Django's built-in `django.contrib.auth` |
| **Server** | Gunicorn 23.0 (production) |
| **Config** | `python-dotenv` for environment variables |
| **Image Handling** | Pillow 12.1 |
| **Deployment** | Railway |

---

## 📁 Project Structure

```
.
├── manage.py
├── requirements.txt
├── .env.example                  # Template — copy to .env and fill in
├── data.json / items.json        # Seed data fixtures
│
├── mysite/                       # Django project config
│   ├── settings.py               # DB, middleware, logging, caching
│   ├── urls.py                   # Root URL routing
│   ├── wsgi.py / asgi.py
│
├── myapp/                        # Food items app
│   ├── models.py                 # Item, Category
│   ├── views.py                  # FBVs + DRF API view
│   ├── forms.py                  # ItemForm with custom validation
│   ├── managers.py               # ItemManager (soft-delete aware)
│   ├── middleware.py             # Logging, timing, IP blocking
│   ├── serializers.py            # DRF ItemSerializer
│   ├── admin.py                  # Django admin registration
│   ├── urls.py
│   ├── migrations/
│   ├── templates/myapp/          # base, index, detail, item-form, item-delete
│   ├── templatetags/             # custom_filters.py (currency filter)
│   └── static/myapp/style.css
│
└── users/                        # Authentication app
    ├── models.py                 # Profile (OneToOne with User)
    ├── views.py                  # register, logout, profile
    ├── forms.py                  # RegisterForm (extends UserCreationForm)
    ├── urls.py
    ├── migrations/
    └── templates/users/          # login, register, logout, profile
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL 13+ (or SQLite — see note below)
- pip and virtualenv

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/foodhub.git
cd foodhub

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file (see template below)
cp .env.example .env
# Then edit .env with your own values

# 5. Apply database migrations
python manage.py migrate

# 6. (Optional) Load seed data
python manage.py loaddata items.json

# 7. Create a superuser for the admin
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/** and will redirect to `/myapp/`.

### `.env.example`

Create a `.env` file in the project root with the following keys:

```env
DJANGO_SECRET_KEY=your-long-random-secret-key-here
DJANGO_DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

> 💡 **Prefer SQLite for local dev?** Uncomment the SQLite `DATABASES` block in `mysite/settings.py` and comment out the PostgreSQL block.

---

## 🔌 URL & API Reference

### Web Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | Redirect | Sends user to `/myapp/` |
| `/myapp/` | `index` | Paginated item catalogue |
| `/myapp/<id>/` | `detail` | Single item page |
| `/myapp/add/` | `create_item` | Form to create a new item (login required) |
| `/myapp/update/<id>/` | `update_Item` | Edit an item (owner only) |
| `/myapp/delete/<id>/` | `delete_Item` | Soft-delete an item (owner only) |
| `/users/register/` | `register` | Sign up |
| `/users/login/` | `LoginView` | Log in |
| `/users/logout/` | `logout_view` | Log out |
| `/users/profile/` | `profile` | View your profile (login required) |
| `/admin/` | Django admin | Superuser-only |

### REST API

| Method | Endpoint | Returns |
|--------|----------|---------|
| `GET` | `/myapp/item-json/` | JSON list of all items via `ItemSerializer` |

Example response:

```json
[
  {
    "id": 21,
    "item_name": "Ice Cream Sundae",
    "item_desc": "Vanilla ice cream topped with chocolate sauce",
    "item_price": "4.59",
    "item_image": "https://www.svgrepo.com/show/66980/fast-food-placeholder.svg"
  }
]
```

---

## 🧠 Django Concepts Demonstrated

This project was an opportunity to put a wide range of Django patterns into practice:

- **ORM & migrations** — 12 incremental migrations evolving the `Item` model
- **Custom model managers** — implementing soft-delete cleanly at the queryset level
- **Function-based views** vs **class-based views** (CBVs retained in comments for reference)
- **ModelForms** with `clean_<field>()` and cross-field `clean()` validation
- **Custom template tags & filters** in `myapp/templatetags/custom_filters.py`
- **Custom middleware** — three independent middleware classes for logging, timing, and access control
- **DRF serializers** and `@api_view` for building a JSON API
- **Pagination** using `django.core.paginator.Paginator`
- **Caching** with the file-based cache backend
- **Logging configuration** with file + console handlers
- **Authentication & authorization** with `@login_required` and ownership checks
- **Database indexing** for performance-critical columns
- **12-factor configuration** via `python-dotenv` and `os.getenv`
- **Production deployment** to Railway with Gunicorn, `STATIC_ROOT`, and `CSRF_TRUSTED_ORIGINS`

---

## 🔒 Security Notes

If you're forking or deploying this project, please address the following before going live:

1. **Never commit `.env`** — add it to `.gitignore` immediately. Use `.env.example` as the committed template.
2. **Load `SECRET_KEY` from the environment** — currently hardcoded in `settings.py`; switch to `os.getenv("DJANGO_SECRET_KEY")`.
3. **Set `DEBUG = False`** in production — drive this from `DJANGO_DEBUG` in `.env`.
4. **Rotate any credentials** that may have been committed in earlier history.
5. **Review `ALLOWED_HOSTS`** to match your production domain only.

---

## 🗺️ Possible Next Steps

- 🏷️ Wire the `Category` model into items (currently defined but unused)
- 🔍 Add search and filter functionality to the catalogue
- 🛒 Build a cart/order workflow on top of the item catalogue
- 🔐 Lock down the REST API with token / session authentication and per-user write endpoints
- 🧪 Add a test suite (currently scaffolded but empty)
- 🐳 Containerise with Docker for parity between local and production environments

---

## 👤 Author

**Darshil Zadaphiya**
MSc Business Analytics — Coventry University

---

## 📝 License

This project is for educational and portfolio purposes. Feel free to fork it and learn from it.
