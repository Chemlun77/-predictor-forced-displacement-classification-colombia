# Deployment Guide - Render.com

This guide provides step-by-step instructions to deploy the Forced Displacement Predictor application on Render.com's free tier.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ GitHub account
- ✅ Render.com account (free - no credit card required)
- ✅ All code pushed to your GitHub repository
- ✅ Google Gemini API key (for chatbot functionality)

---

## ⚠️ Important Notes Before Deployment

### Random Forest Model Limitation

**The Random Forest model (3.9 GB) is NOT included in deployment** due to Render's free tier memory limitations (512 MB RAM).

**What this means:**
- ✅ **Local installation:** All 5 models available
- ⚠️ **Deployed version:** 4 models available (Logistic Regression, XGBoost, ResNet-Style, Deep)
- ❌ **Random Forest:** Will show error message if selected

**Why?**
- Random Forest model size: 3.9 GB
- Render free tier RAM: 512 MB
- Other models combined: < 50 MB

---

## 🚀 Step 1: Prepare Your Repository

### 1.1 Create Required Files

You should already have these files created:

**File 1: `backend/requirements.txt`**
```txt
Flask==3.0.0
Flask-CORS==4.0.0
pandas==2.2.0
numpy==1.26.0
scikit-learn==1.5.0
tensorflow==2.17.0
xgboost==2.1.0
joblib==1.3.2
sodapy==2.2.0
google-generativeai==0.8.3
gunicorn==21.2.0
```

**File 2: `render.yaml` (in project root)**
```yaml
services:
  # Backend API
  - type: web
    name: displacement-predictor-api
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "cd 01_displacement_web/backend && pip install -r requirements.txt"
    startCommand: "cd 01_displacement_web/backend && gunicorn app:app --bind 0.0.0.0:$PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: FLASK_ENV
        value: production
    healthCheckPath: /api/models

  # Frontend Static Site
  - type: web
    name: displacement-predictor-frontend
    env: static
    region: oregon
    plan: free
    branch: main
    buildCommand: "cd 01_displacement_web/frontend && npm install && npm run build"
    staticPublishPath: 01_displacement_web/frontend/build
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

**File 3: `01_displacement_web/frontend/.env.production`**
```env
REACT_APP_API_URL=https://displacement-predictor-api.onrender.com
```

### 1.2 Update Frontend API Configuration

**Edit: `frontend/src/services/apiService.js`**

Find the line with `API_BASE_URL` and update it:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';
```

**Edit: `frontend/src/services/chatService.js`**

Find the line with `API_BASE_URL` and update it:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api/chat`
  : 'http://127.0.0.1:5000/api/chat';
```

### 1.3 Verify .gitignore

Ensure your `.gitignore` includes:
```gitignore
# Exclude Random Forest model (too large for deployment)
01_displacement_web/db/02a_classical_models/saved_models/Random_Forest_best_model.pkl

# Keep other models
!01_displacement_web/db/02a_classical_models/saved_models/Logistic_Regression_best_model.pkl
!01_displacement_web/db/02a_classical_models/saved_models/XGBoost_best_model.pkl
!01_displacement_web/db/02a_classical_models/saved_models/categorical_encoders.pkl
!01_displacement_web/db/02a_classical_models/saved_models/numeric_scalers.pkl
!01_displacement_web/db/02b_neural_networks/saved_models/*.keras
!01_displacement_web/db/02b_neural_networks/saved_models/*.pkl
```

### 1.4 Push Everything to GitHub
```bash
# Add all files
git add .

# Commit changes
git commit -m "Prepare for Render deployment"

# Push to GitHub
git push origin main
```

**⚠️ IMPORTANT:** Make sure Random Forest model is NOT pushed (check file sizes).

---

## 🌐 Step 2: Deploy to Render.com

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your repositories

### 2.2 Create New Blueprint

1. In Render dashboard, click **"New +"** (top right)
2. Select **"Blueprint"**
3. Connect your GitHub repository:
   - Select your repository: `predictor-forced-displacement-classification-colombia`
   - Branch: `main`
4. Click **"Apply"**

**What happens next:**
- Render reads your `render.yaml` file
- Creates TWO services automatically:
  - `displacement-predictor-api` (Backend)
  - `displacement-predictor-frontend` (Frontend)

### 2.3 Monitor Deployment

You'll see two services deploying:

**Backend (API):**
- Build time: ~10-15 minutes
- Status shows: "Building..." → "Deploying..." → "Live"
- URL: `https://displacement-predictor-api.onrender.com`

**Frontend:**
- Build time: ~5-10 minutes
- Status shows: "Building..." → "Deploying..." → "Live"
- URL: `https://displacement-predictor-frontend.onrender.com`

**Click on each service to see build logs and troubleshoot if needed.**

---

## 🔧 Step 3: Configure Services

### 3.1 Backend Configuration

1. Click on `displacement-predictor-api` service
2. Go to **"Environment"** tab
3. Verify environment variables:
   - `PYTHON_VERSION`: 3.10.0
   - `FLASK_ENV`: production

**No additional configuration needed!**

### 3.2 Frontend Configuration

1. Click on `displacement-predictor-frontend` service
2. Go to **"Settings"** tab
3. Verify build settings:
   - **Build Command:** `cd 01_displacement_web/frontend && npm install && npm run build`
   - **Publish Directory:** `01_displacement_web/frontend/build`

**Environment variables are read from `.env.production` automatically.**

---

## ✅ Step 4: Verify Deployment

### 4.1 Test Backend

Visit: `https://displacement-predictor-api.onrender.com/api/models`

**Expected response:**
```json
{
  "models": [
    {"name": "Logistic_Regression", "display": "Logistic Regression"},
    {"name": "Random_Forest", "display": "Random Forest"},
    {"name": "XGBoost", "display": "XGBoost"},
    {"name": "ResNet_Style", "display": "ResNet Style"},
    {"name": "Deep", "display": "Deep (Wide & Deep)"}
  ]
}
```

**Note:** Random Forest appears in the list but will show error if selected.

### 4.2 Test Frontend

Visit: `https://displacement-predictor-frontend.onrender.com`

**You should see:**
- ✅ Application loads
- ✅ Map displays
- ✅ Model dropdown shows all 5 models
- ✅ Variables load correctly

### 4.3 Test Full Workflow

1. **Select a model** (use XGBoost or Logistic Regression)
2. **Fill in variables:**
   - Department: Any (e.g., Antioquia)
   - Gender: Any
   - Ethnicity: Any
   - Disability: Any
   - Age group: Any
   - Year: 2010
   - Events: 5
3. **Click "Predecir"**
4. **Check results:**
   - ✅ Prediction displays
   - ✅ Map updates
   - ✅ Validation info shows

5. **Test Chatbot:**
   - Click "💬 AI Assistant"
   - Provide Gemini API key
   - Request explanation
   - ✅ AI explanation generates

### 4.4 Test Random Forest Warning

1. Select **"Random Forest"** from dropdown
2. Fill in variables
3. Click "Predecir"
4. **Expected:** Error message about model not available in deployment

---

## 🐛 Troubleshooting

### Issue 1: Backend Build Failed

**Symptoms:** Backend shows "Build failed" in Render dashboard

**Solutions:**
1. Check build logs in Render dashboard
2. Verify `requirements.txt` has correct versions
3. Ensure Python version is 3.10.0
4. Check that models are pushed to GitHub (except Random Forest)

**Common errors:**
- `ModuleNotFoundError`: Missing dependency in requirements.txt
- `Memory error`: Model too large (should only happen if Random Forest was included)

### Issue 2: Frontend Build Failed

**Symptoms:** Frontend shows "Build failed" in Render dashboard

**Solutions:**
1. Check build logs
2. Verify `package.json` exists in `frontend/` directory
3. Check that `npm install` completes successfully
4. Ensure React build command is correct

### Issue 3: CORS Errors

**Symptoms:** Frontend can't connect to backend, console shows CORS errors

**Solutions:**
1. Verify backend has `Flask-CORS` installed
2. Check that backend `app.py` has `CORS(app)` enabled
3. Verify `.env.production` has correct backend URL

### Issue 4: Models Not Loading

**Symptoms:** Prediction fails with "Model not found" error

**Solutions:**
1. Check that models are in repository:
```bash
   git ls-files | grep "\.pkl$\|\.keras$"
```
2. Verify `.gitignore` is not excluding needed models
3. Check Render logs for model loading errors

### Issue 5: Free Tier Sleep

**Symptoms:** First visit takes 30-60 seconds to load

**Solution:** This is normal behavior for Render's free tier
- Services sleep after 15 minutes of inactivity
- First request wakes the service (takes ~30-60 seconds)
- Subsequent requests are fast
- No action needed - explain this to evaluators

---

## 📊 Understanding Free Tier Limitations

### Render Free Tier Specs:
- **RAM:** 512 MB
- **CPU:** Shared
- **Build Time:** 500 hours/month
- **Bandwidth:** 100 GB/month
- **Sleep:** After 15 min inactivity
- **Wake Time:** ~30-60 seconds

### What This Means:
- ✅ Perfect for evaluation (< 1 week, minimal traffic)
- ✅ Handles ~1000 predictions/day easily
- ⚠️ First visit each session takes time to wake
- ❌ Can't include Random Forest (too large)

---

## 🔄 Updating Your Deployment

### After Making Code Changes:

1. **Commit and push to GitHub:**
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

2. **Automatic Redeployment:**
   - Render detects the push automatically
   - Rebuilds both services
   - Deploys new version
   - Takes ~10-15 minutes

3. **Manual Redeploy (if needed):**
   - Go to Render dashboard
   - Click on service
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 🎥 Preparing for Evaluation

### Information to Share with Evaluators:

**Live Application:**
- URL: `https://displacement-predictor-frontend.onrender.com`
- **First Visit:** May take 30-60 seconds (service waking from sleep)
- **Subsequent Visits:** Fast response

**Important Notes:**
1. **Random Forest:** Not available in deployment (memory limitations)
2. **Cold Starts:** Normal for free tier
3. **Gemini API Key:** Users must provide their own free API key
4. **Data Source:** Real-time from datos.gov.co API

**Suggested Evaluation Path:**
1. Visit application URL
2. Wait for initial load (~30-60 sec)
3. Select **XGBoost** or **Logistic Regression** model
4. Make prediction with sample data
5. Test chatbot with Gemini API key
6. Explore interactive map
7. Make additional predictions (fast)

---

## 📈 Monitoring Your Deployment

### In Render Dashboard:

**Metrics Available:**
- Requests per second
- Response times
- Memory usage
- Error rates

**Logs Available:**
- Build logs
- Application logs
- Error logs

**How to Access:**
1. Go to Render dashboard
2. Click on service
3. Click "Logs" or "Metrics" tab

---

## 🔒 Security Considerations

### Current Setup:
- ✅ HTTPS enabled automatically (Render provides SSL)
- ✅ CORS configured for frontend domain
- ✅ No sensitive data stored in repository
- ✅ API keys provided by users (not stored)

### Production Recommendations (if extending beyond evaluation):
- Add rate limiting
- Implement API authentication
- Add error monitoring (Sentry, etc.)
- Set up custom domain
- Upgrade to paid tier for production use

---

## 💰 Cost Analysis

### Free Tier (Current):
- **Cost:** $0/month
- **Duration:** Unlimited
- **Limitations:** Sleep after inactivity, 512 MB RAM
- **Best For:** Evaluation, demos, personal projects

### If You Need More:
- **Starter Plan:** $7/month per service
- **Benefits:** 1 GB RAM, no sleep, faster builds
- **When to Upgrade:** Production use, more traffic

---

## 📞 Support Resources

### If You Need Help:

**Render Documentation:**
- [Render Docs](https://render.com/docs)
- [Blueprints Guide](https://render.com/docs/blueprint-spec)
- [Python Deployment](https://render.com/docs/deploy-flask)
- [Static Sites](https://render.com/docs/static-sites)

**GitHub Issues:**
- Open issue in your repository
- Include error logs from Render dashboard

**Community:**
- [Render Community Forum](https://community.render.com)

---

## ✅ Deployment Checklist

Before considering deployment complete:

- [ ] Backend deploys successfully
- [ ] Frontend deploys successfully
- [ ] Backend health check passes
- [ ] Frontend connects to backend
- [ ] Predictions work (except Random Forest)
- [ ] Map displays correctly
- [ ] Chatbot connects (with API key)
- [ ] Validation with RUV data works
- [ ] Random Forest shows appropriate error
- [ ] URLs shared with evaluators
- [ ] Cold start behavior explained

---

## 🎉 Success!

If all checks pass, your application is successfully deployed!

**Share these URLs with evaluators:**
- **Application:** `https://displacement-predictor-frontend.onrender.com`
- **API:** `https://displacement-predictor-api.onrender.com`
- **Repository:** `https://github.com/Chemlun77/-predictor-forced-displacement-classification-colombia`

**Remember to mention:**
- Free tier cold start (30-60 sec first visit)
- Random Forest not available in deployment
- Users need own Gemini API key for chatbot

---

**Need help? Open an issue on GitHub or check Render documentation.**