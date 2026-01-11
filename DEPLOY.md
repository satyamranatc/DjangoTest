# Deploy to Render

## Quick Setup Steps

### 1. Push Your Changes to GitHub

```bash
git add .
git commit -m "Configure for Render deployment"
git push
```

### 2. Create New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `satyamranatc/DjangoTest`

### 3. Configure the Web Service

- **Name**: `djangotest-api` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn core.wsgi:application`

### 4. Add Environment Variables

Click **"Advanced"** and add these environment variables:

| Key              | Value                                                               |
| ---------------- | ------------------------------------------------------------------- |
| `PYTHON_VERSION` | `3.14.0`                                                            |
| `SECRET_KEY`     | Generate a new secret key (use [djecrety.ir](https://djecrety.ir/)) |
| `DEBUG`          | `False`                                                             |
| `ALLOWED_HOSTS`  | Your Render URL (e.g., `djangotest-api.onrender.com`)               |

### 5. Deploy

- Click **"Create Web Service"**
- Wait for deployment to complete (~5-10 minutes)

### 6. Access Your API

Your API will be available at:

- `https://your-app-name.onrender.com/api/test-data/`

## Notes

- Free tier services spin down after 15 minutes of inactivity
- First request after inactivity may take 30-60 seconds
- Database is SQLite (for production, consider upgrading to PostgreSQL)
