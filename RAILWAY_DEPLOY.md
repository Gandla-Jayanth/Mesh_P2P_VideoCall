# Railway Deployment Steps

## Step 1: Push to GitHub
1. Create a new repository on GitHub (don't initialize with README)
2. Copy the repository URL
3. Run these commands:
```bash
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Railway
1. Go to https://railway.app
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your repository
6. Railway will auto-detect Python and deploy

## Step 3: Configure Environment Variables (Optional but Recommended)
In Railway dashboard → Your Project → Variables tab, add:
- `SECRET_KEY`: Generate a random secret key (use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Set to your Railway domain (e.g., `yourapp.railway.app`)

## Step 4: Add Redis (Optional - for production WebSocket scaling)
1. In Railway dashboard → New → Database → Add Redis
2. Copy the Redis URL
3. Add environment variable: `REDIS_URL` = your Redis connection string

## Step 5: Run Migrations
In Railway dashboard → Your Service → Deployments → View Logs, you'll see the build process.

After deployment, go to Railway dashboard → Your Service → Settings → Deploy Command, add:
```
python manage.py migrate && daphne -b 0.0.0.0 -p $PORT videocall.asgi:application
```

Or run migrations manually via Railway CLI or one-off command.

## Your app will be live at: https://YOUR_PROJECT_NAME.up.railway.app

