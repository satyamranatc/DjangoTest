# Complete Guide: Django DRF to Render Deployment

This guide covers everything from creating a Django REST Framework project to deploying it on Render.

---

## Part 1: Create Django DRF Project

### Step 1: Set Up Virtual Environment

```bash
# Navigate to your project directory
cd ~/Desktop/DjangoTest

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Mac/Linux
# .venv\Scripts\activate   # On Windows
```

### Step 2: Install Django and DRF

```bash
pip install django djangorestframework
```

### Step 3: Create Django Project and App

```bash
# Create Django project (the . creates it in current directory)
django-admin startproject core .

# Create an app for your API
python manage.py startapp api
```

### Step 4: Configure Settings

Edit `core/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add this
    'api',             # Add this
]
```

### Step 5: Create Your API View

Edit `api/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hardcoded_test_view(request):
    data = {
        "message": "This is hardcoded data for testing!",
        "status": "success",
        "data": {
            "user": "Your Name",
            "technologies": ["Django", "DRF", "Python"]
        }
    }
    return Response(data)
```

### Step 6: Configure URLs

Create `api/urls.py`:

```python
from django.urls import path
from .views import hardcoded_test_view

urlpatterns = [
    path('test-data/', hardcoded_test_view, name='test_data'),
]
```

Edit `core/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Add this
]
```

### Step 7: Test Locally

```bash
# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Test in browser or curl
# Visit: http://127.0.0.1:8000/api/test-data/
```

---

## Part 2: Prepare for Deployment

### Step 1: Install Production Dependencies

```bash
pip install gunicorn whitenoise psycopg2-binary
```

### Step 2: Generate requirements.txt

```bash
pip freeze > requirements.txt
```

### Step 3: Update Settings for Production

Edit `core/settings.py`:

**Add imports at the top:**

```python
from pathlib import Path
import os  # Add this
```

**Update security settings:**

```python
# Use environment variables for security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-dev-secret-key')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

**Add WhiteNoise to middleware (add right after SecurityMiddleware):**

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware
]
```

**Configure static files at the bottom:**

```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise configuration
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### Step 4: Create Build Script

Create `build.sh` in the root directory:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:

```bash
chmod +x build.sh
```

### Step 5: Create .gitignore

Create `.gitignore`:

```
# Python
*.pyc
__pycache__/
*.py[cod]
.Python

# Virtual Environment
.venv/
venv/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/

# IDEs
.vscode/
.idea/

# OS
.DS_Store
```

### Step 6: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial Django DRF project"

# Add remote (replace with your repository URL)
git remote add origin git@github.com:yourusername/yourrepo.git

# Push to GitHub
git push -u origin main
```

---

## Part 3: Deploy to Render

### Step 1: Sign Up / Log In to Render

- Go to [https://render.com](https://render.com)
- Sign up or log in (you can use GitHub to sign in)

### Step 2: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 3: Connect Your Repository

1. Click **"Connect account"** if you haven't connected GitHub yet
2. Find and select your repository (e.g., `yourusername/DjangoTest`)
3. Click **"Connect"**

### Step 4: Configure Web Service

Fill in the following settings:

| Field              | Value                                            |
| ------------------ | ------------------------------------------------ |
| **Name**           | `your-project-name` (e.g., `djangotest-api`)     |
| **Region**         | Choose closest to you (e.g., `Oregon (US West)`) |
| **Branch**         | `main`                                           |
| **Root Directory** | Leave blank                                      |
| **Runtime**        | `Python 3`                                       |
| **Build Command**  | `./build.sh`                                     |
| **Start Command**  | `gunicorn core.wsgi:application`                 |
| **Instance Type**  | `Free`                                           |

### Step 5: Add Environment Variables

Click **"Advanced"** to expand advanced settings, then scroll to **"Environment Variables"**:

Click **"Add Environment Variable"** and add these:

| Key              | Value                   | Notes                                   |
| ---------------- | ----------------------- | --------------------------------------- |
| `PYTHON_VERSION` | `3.14.0`                | Or your Python version                  |
| `SECRET_KEY`     | Generate new secret key | Use [djecrety.ir](https://djecrety.ir/) |
| `DEBUG`          | `False`                 | Never True in production!               |
| `ALLOWED_HOSTS`  | `.onrender.com`         | Will allow all Render subdomains        |

**To generate SECRET_KEY:**

- Visit [https://djecrety.ir/](https://djecrety.ir/)
- Copy the generated key
- Paste it as the value for `SECRET_KEY`

### Step 6: Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Render will start deploying your application
3. Wait 5-10 minutes for the build to complete

### Step 7: Monitor Deployment

- You'll see the build logs in real-time
- Look for messages like:
  - `Installing dependencies...`
  - `Collecting static files...`
  - `Running migrations...`
  - `Your service is live 🎉`

### Step 8: Access Your API

Once deployed, your API will be available at:

```
https://your-project-name.onrender.com/api/test-data/
```

For example:

```
https://djangotest-api.onrender.com/api/test-data/
```

---

## Part 4: Post-Deployment

### Update ALLOWED_HOSTS

After getting your Render URL, update the environment variable:

1. Go to your Render dashboard
2. Click on your web service
3. Go to **"Environment"** tab
4. Update `ALLOWED_HOSTS` with your actual URL:
   ```
   your-app-name.onrender.com
   ```
5. Save changes (this will trigger a redeploy)

### Test Your API

```bash
# Test with curl
curl https://your-app-name.onrender.com/api/test-data/

# Or visit in browser
# https://your-app-name.onrender.com/api/test-data/
```

---

## Important Notes

### Free Tier Limitations

- ⏰ **Spin down after 15 minutes** of inactivity
- 🐌 **First request after inactivity** takes 30-60 seconds (cold start)
- 💾 **750 hours/month** of usage (enough for one service running 24/7)

### Database Consideration

- 📦 Currently using **SQLite** (file-based)
- ⚠️ SQLite data is **NOT persistent** on Render free tier
- 🔄 Data will be **lost on each deploy**
- 🎯 For production, upgrade to **PostgreSQL** (Render offers free PostgreSQL tier too)

### Updating Your Deployment

Whenever you push changes to GitHub:

```bash
git add .
git commit -m "Your changes"
git push
```

Render will **automatically redeploy** your application!

---

## Troubleshooting

### Build Failed

- Check the build logs for errors
- Ensure `requirements.txt` is up to date
- Verify `build.sh` has correct permissions

### Service Won't Start

- Check `gunicorn core.wsgi:application` matches your project structure
- Verify environment variables are set correctly
- Check application logs in Render dashboard

### 500 Internal Server Error

- Set `DEBUG=True` temporarily to see error details (remember to set back to `False`)
- Check logs in Render dashboard
- Ensure all migrations have run

### API Not Accessible

- Verify ALLOWED_HOSTS includes your Render domain
- Check that URLs are configured correctly
- Make sure your service is running (not suspended)

---

## What's Next?

### Add PostgreSQL Database

1. Create **PostgreSQL** instance on Render
2. Update `settings.py` to use PostgreSQL
3. Add database URL to environment variables

### Add CORS for Frontend

```bash
pip install django-cors-headers
```

Update settings to allow frontend access.

### Add Authentication

- Django REST Framework Token Authentication
- JWT Authentication
- OAuth2

### Custom Domain

- Add your custom domain in Render settings
- Update ALLOWED_HOSTS accordingly

---

## Quick Reference Commands

```bash
# Local Development
source .venv/bin/activate
python manage.py runserver

# Update Dependencies
pip freeze > requirements.txt

# Deploy Changes
git add .
git commit -m "Update"
git push

# Generate New Secret Key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

**🎉 Congratulations! Your Django DRF API is now live on Render!**
