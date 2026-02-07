# HR Evaluation System - Deployment Guide

## 🚀 Deployment Configuration

This guide will help you deploy the HR Evaluation System with:
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: Render PostgreSQL

---

## 📋 Prerequisites

1. GitHub account
2. Vercel account (free tier available)
3. Render account (free tier available)
4. Supabase account (for file storage)
5. Groq API key (for AI features)

---

## 🎯 Backend Deployment (Render)

### Step 1: Prepare Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `hr-evaluation-db`
   - **Database**: `hr_evaluation`
   - **User**: `hr_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click "Create Database"
5. **Save** the "Internal Database URL" from the database page

### Step 2: Deploy Backend

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `hr-evaluation-backend`
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main` (or your deployment branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free (or paid for production)

5. **Environment Variables** (Add in Render dashboard):
   ```
   DATABASE_URL=<paste_internal_database_url_from_step1>
   SECRET_KEY=<generate_random_string>
   JWT_SECRET=<generate_random_string>
   JWT_EXP_MINUTES=1440
   SUPABASE_URL=<your_supabase_project_url>
   SUPABASE_KEY=<your_supabase_anon_key>
   SUPABASE_BUCKET=uploads
   GROQ_API_KEY=<your_groq_api_key>
   FRONTEND_URL=https://your-app.vercel.app
   ```

6. Click "Create Web Service"
7. Wait for deployment to complete
8. **Save your backend URL** (e.g., `https://hr-evaluation-backend.onrender.com`)

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 2: Environment Variables

Add the following environment variable in Vercel:

```
VITE_API_URL=https://hr-evaluation-backend.onrender.com
```

(Use your actual Render backend URL from previous step)

### Step 3: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. **Save your frontend URL** (e.g., `https://hr-evaluation.vercel.app`)

### Step 4: Update Backend CORS

1. Go back to Render dashboard
2. Open your backend service
3. Update the `FRONTEND_URL` environment variable:
   ```
   FRONTEND_URL=https://hr-evaluation.vercel.app
   ```
4. Save and wait for redeployment

---

## 🔧 Post-Deployment Configuration

### 1. Test the Deployment

1. Visit your Vercel frontend URL
2. Test the following:
   - Recruiter registration/login
   - Candidate login
   - File uploads
   - API connectivity

### 2. Set Up Supabase Storage

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project or select existing
3. Go to Storage → Create bucket named `uploads`
4. Set bucket to **Public** or configure policies for authenticated access
5. Copy your project URL and anon key to Render environment variables

### 3. Monitor Logs

- **Render Logs**: Check backend logs in Render dashboard
- **Vercel Logs**: Check frontend logs in Vercel dashboard

---

## ⚙️ Environment Variables Summary

### Backend (Render)
```env
DATABASE_URL=<postgresql_connection_string>
SECRET_KEY=<random_secret_key>
JWT_SECRET=<random_jwt_secret>
JWT_EXP_MINUTES=1440
SUPABASE_URL=<supabase_project_url>
SUPABASE_KEY=<supabase_anon_key>
SUPABASE_BUCKET=uploads
GROQ_API_KEY=<groq_api_key>
FRONTEND_URL=<vercel_frontend_url>
```

### Frontend (Vercel)
```env
VITE_API_URL=<render_backend_url>
```

---

## 🐛 Troubleshooting

### CORS Errors
- Check that `FRONTEND_URL` in Render matches your Vercel URL exactly
- Ensure no trailing slashes in URLs

### Database Connection Issues
- Verify `DATABASE_URL` is correct in Render
- Check that database is in the same region as web service
- Ensure database is running

### Build Failures
- Check build logs in Render/Vercel
- Verify all dependencies are in `requirements.txt`/`package.json`
- Ensure Python version matches (3.12+)

### API Not Working
- Verify `VITE_API_URL` in Vercel environment variables
- Check backend logs in Render for errors
- Test backend endpoint directly: `https://your-backend.onrender.com/api/health`

---

## 📱 Production Considerations

1. **Security**:
   - Use strong SECRET_KEY and JWT_SECRET
   - Restrict CORS to specific domains
   - Enable HTTPS only

2. **Performance**:
   - Upgrade to paid Render plan for no cold starts
   - Consider CDN for static assets
   - Optimize database queries

3. **Monitoring**:
   - Set up error tracking (e.g., Sentry)
   - Monitor API response times
   - Set up uptime monitoring

4. **Backups**:
   - Enable automatic database backups in Render
   - Version control all code changes
   - Document environment variables

---

## 🎉 Deployment Complete!

Your HR Evaluation System is now live:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.onrender.com`

Remember to update your README with the live URLs!
