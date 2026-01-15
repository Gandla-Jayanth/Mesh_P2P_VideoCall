# Deployment Guide: Mesh P2P Python Application

## ⚠️ Important Limitation

**Netlify cannot host Django applications with WebSocket support.** This application requires:
- Django backend server
- WebSocket connections (for real-time P2P signaling)
- Persistent connections

## Solution: Hybrid Deployment

Deploy the **frontend** on Netlify and the **backend** on a platform that supports Django + WebSockets.

---

## Part 1: Deploy Backend (Django + WebSockets)

### Option A: Deploy to Render (Recommended - Free Tier Available)

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Prepare Your Backend**
   - Push your code to GitHub
   - Make sure `requirements.txt` exists in the root

3. **Create a New Web Service on Render**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository with your Django app

4. **Configure Build Settings**
   ```
   Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
   Start Command: daphne -b 0.0.0.0:$PORT videocall.asgi:application
   ```

5. **Set Environment Variables**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL (e.g., `https://your-app.onrender.com`)

---

### Option B: Deploy to Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Django
   - Add environment variables:
     ```
     SECRET_KEY=your-secret-key
     DEBUG=False
     ```
   - Set start command: `daphne -b 0.0.0.0:$PORT videocall.asgi:application`

4. **Deploy**
   - Railway will auto-deploy
   - Copy your backend URL

---

### Option C: Deploy to Fly.io

1. **Install Fly CLI**
   ```bash
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Initialize**
   ```bash
   cd "Mesh p2p python/Mesh p2p python"
   fly launch
   ```

4. **Create fly.toml** (if not auto-generated)
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[services]]
     protocol = "tcp"
     internal_port = 8000
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

---

## Part 2: Deploy Frontend to Netlify

### Step 1: Prepare Frontend Files

The frontend files are already prepared in the `public/` directory.

### Step 2: Create Netlify Account

1. Go to https://netlify.com
2. Sign up (GitHub, GitLab, or Email)

### Step 3: Deploy via Netlify Dashboard

1. **Log in to Netlify Dashboard**
   - Go to https://app.netlify.com

2. **Add New Site**
   - Click "Add new site" → "Deploy manually"
   - Or connect to Git for continuous deployment

3. **Upload Files**
   - Drag and drop the `public` folder
   - Or use the Netlify CLI (see below)

4. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add: `BACKEND_URL` = `https://your-backend-url.onrender.com`
   - (Replace with your actual backend URL)

5. **Configure Redirects**
   - The `netlify.toml` file is already configured
   - It handles SPA routing

### Step 4: Update Frontend to Use Backend URL

The `public/index.html` file needs to know your backend URL. You have two options:

**Option A: Use Netlify Environment Variable (Recommended)**
- The HTML file will read from `window.BACKEND_URL`
- Set it via Netlify's environment variables
- Or inject it during build (see below)

**Option B: Hardcode in HTML**
- Edit `public/index.html`
- Replace `'https://your-backend-url.herokuapp.com'` with your actual backend URL

### Step 5: Deploy via Netlify CLI (Alternative)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd "Mesh p2p python/Mesh p2p python"
netlify deploy --prod --dir=public
```

---

## Part 3: Configure CORS (Important!)

Your backend needs to allow requests from your Netlify frontend.

### Update Django Settings

Add to `videocall/settings.py`:

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "https://your-netlify-app.netlify.app",
    "http://localhost:8888",  # For local testing
]

# Or allow all (less secure, for development)
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!
```

Install django-cors-headers:
```bash
pip install django-cors-headers
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
```

Add to `MIDDLEWARE` (at the top):
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this first
    'django.middleware.security.SecurityMiddleware',
    ...
]
```

---

## Part 4: Update Requirements

Make sure your `requirements.txt` includes:

```
Django>=4.2.0,<5.0.0
channels>=4.0.0
daphne>=4.0.0
channels-redis>=4.1.0
asgiref>=3.6.0
django-cors-headers>=4.0.0
```

---

## Part 5: Testing

1. **Test Backend**
   - Visit: `https://your-backend-url.onrender.com`
   - Should see Django page or your app

2. **Test Frontend**
   - Visit: `https://your-netlify-app.netlify.app`
   - Open browser console
   - Check WebSocket connection to backend

3. **Test Full Flow**
   - Open two browser windows
   - Both should connect to WebSocket
   - Start video calls between them

---

## Troubleshooting

### WebSocket Connection Failed
- Check backend URL is correct
- Verify CORS settings
- Check backend logs for errors

### CORS Errors
- Add your Netlify URL to `CORS_ALLOWED_ORIGINS`
- Restart backend server

### 404 Errors on Netlify
- Check `netlify.toml` redirects configuration
- Ensure `public/index.html` exists

### Backend Not Starting
- Check environment variables are set
- Verify `requirements.txt` is correct
- Check build logs on your hosting platform

---

## Quick Reference URLs

After deployment, you'll have:
- **Frontend**: `https://your-app.netlify.app`
- **Backend**: `https://your-app.onrender.com` (or Railway/Fly.io)

Update the frontend's `BACKEND_URL` to point to your backend!

---

## Alternative: Single Platform Deployment

If you want everything on one platform (not Netlify), consider:
- **Render** (supports both frontend and backend)
- **Railway** (supports both)
- **Fly.io** (supports both)
- **Heroku** (paid, but reliable)

These platforms can host your entire Django app including the frontend templates.
