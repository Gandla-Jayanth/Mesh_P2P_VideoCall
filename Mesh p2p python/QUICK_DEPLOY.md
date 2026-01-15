# ⚡ Quick Deployment Guide

## 🚨 Why Not Netlify?

**Netlify cannot run Django applications with WebSockets.** Your app needs:
- ✅ A Python runtime (Django)
- ✅ WebSocket support (for real-time video)
- ✅ Persistent server process

**Netlify only supports:** Static sites and serverless functions.

## 🎯 Best Option: Railway (5 Minutes)

### Step 1: Push to GitHub
```bash
cd "C:\Users\Dell\Downloads\Mesh p2p python (1)\Mesh p2p python\Mesh p2p python"
git init
git add .
git commit -m "Ready for deployment"
# Create a repo on GitHub and push
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to: https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Django and deploys!

### Step 3: Add Environment Variables
In Railway dashboard → Variables tab:
```
SECRET_KEY=<generate-random-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

Generate secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Run Migrations
In Railway dashboard → Deployments → View Logs, or use CLI:
```bash
railway run python manage.py migrate
```

**Done!** Your app is live at `https://your-app.railway.app` 🎉

---

## 📋 Alternative: Render (Free Tier)

1. Go to: https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
5. Start Command: `daphne -b 0.0.0.0 -p $PORT videocall.asgi:application`
6. Add environment variables (same as Railway)
7. Deploy!

**Note:** Free tier spins down after 15 min inactivity.

---

## 📁 Files Created for Deployment

✅ `requirements.txt` - Python dependencies
✅ `Procfile` - Tells platform how to run your app
✅ `runtime.txt` - Python version
✅ `railway.json` - Railway configuration
✅ `render.yaml` - Render configuration
✅ `.gitignore` - Git ignore rules
✅ `DEPLOYMENT_GUIDE.md` - Full detailed guide

---

## 🆘 Need Help?

See `DEPLOYMENT_GUIDE.md` for detailed instructions and troubleshooting.

