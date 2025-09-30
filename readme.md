# 🛒 Django Shop

A simple and extensible **single-vendor e-commerce web application** built with **Django**.  
This project demonstrates the core features of an online shop: product catalog, shopping cart, order processing, and admin management.

---

## Overview

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)

## Installation & Setup

1. **Clone the repository**:
    ```bash
    git clone git@github.com:PooyaRezaee/django-shop.git
    cd django-shop
    ```

2. **Create virtual environment & install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configure environment variables**:  
   Copy `.env.sample` to `.env` and update the values (e.g. database, secret key):
    ```bash
    cp .env.sample .env
    ```

4. **Create the database**:
    ```bash
    createdb django_shop
    ```

5. **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser** (for admin panel):
    ```bash
    python manage.py createsuperuser
    ```

7. **(Optional) Load sample demo data**:
    ```bash
    python manage.py fill_sample_data
    ```

8. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

---

### 🔹 Access
- WebShop: 👉 [http://localhost:8000/](http://localhost:8000/)  
- Admin dashboard: 👉 [http://localhost:8000/admin/](http://localhost:8000/admin/)  
