# Auto OTP System

A complete Django project implementing a Forgot Password system with OTP verification via SMTP.

## Features
- **Custom User Model**: Uses email as the username.
- **OTP System**: 6-digit code, 5-minute expiry, attempt limiting, and resend functionality.
- **Production Ready**: Supports SQLite for local dev and MySQL for production.
- **Modern UI**: Styled with Tailwind CSS for a premium, responsive look.
- **Secure**: CSRF protection, hashed passwords, secure OTP storage.

## Setup Instructions

### 1. Prerequisite
Ensure you have Python installed.

### 2. Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Environment Configuration
1. Open `.env` and configure your SMTP settings:
   - For Gmail: Use an "App Password" (not your main password).
   - Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`.

### 4. Database Setup
1. Run migrations:
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

### 5. Run the Application
1. Start the server:
   ```bash
   python manage.py runserver
   ```
2. Visit `http://127.0.0.1:8000`

## Production Hosting (Linux/MySQL)
1. Install `mysql-server` on your Linux machine.
2. Create a database: `CREATE DATABASE secure_auth_db;`
3. Update `.env` with production credentials:
   ```env
   DB_NAME=secure_auth_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   ```
4. Set `DEBUG=False` and `ALLOWED_HOSTS` to your domain.
5. Use `gunicorn` and `Nginx` for serving.
## Render Deployment
1. **Build Command**: `pip install -r requirements.txt`
2. **Start Command**: `gunicorn auto_otp.wsgi:application --bind 0.0.0.0:$PORT`
3. **Environment Variables**:
   - `PYTHON_VERSION`: `3.14.3` (or your preferred version)
   - `SECRET_KEY`: `your-secret-key`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
   - `EMAIL_HOST_USER`: `your-email@gmail.com`
   - `EMAIL_HOST_PASSWORD`: `your-app-password`
