# Railway Deployment Instructions

## Backend API Deployment
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo" or "Deploy from CLI"
3. For CLI deployment:
   ```bash
   railway login
   cd backend
   railway deploy
   ```
4. Set environment variables:
   - `DATABASE_URL`: sqlite:///app/weather_dashboard.db
   - `MODEL_SERVER_URL`: [Your model server URL]
   - `SECRET_KEY`: [Generate a secure key]

## Model Server Deployment
1. Create new Railway project for model server
2. Deploy from model-server directory:
   ```bash
   cd model-server
   railway deploy
   ```
3. No additional environment variables needed

## Post-Deployment
1. Get the URLs from Railway dashboard
2. Update frontend API configuration with backend URL
3. Test both services:
   - Backend: `/health` endpoint
   - Model Server: `/health` endpoint

## Service URLs
- Backend API: [Railway will provide URL]
- Model Server: [Railway will provide URL]