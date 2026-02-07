# Deployment Checklist

## Before Deployment

### Backend
- [ ] All environment variables configured in `.env.example`
- [ ] `gunicorn` added to `requirements.txt`
- [ ] Database migrations tested
- [ ] Health check endpoint working (`/api/health`)
- [ ] CORS configured for production domain
- [ ] SECRET_KEY and JWT_SECRET are strong and unique
- [ ] All sensitive data removed from code

### Frontend
- [ ] `VITE_API_URL` environment variable configured
- [ ] Build tested locally (`npm run build`)
- [ ] All API endpoints use environment variable
- [ ] No hardcoded API URLs in code
- [ ] Error handling implemented
- [ ] Loading states implemented

### Database
- [ ] PostgreSQL database created
- [ ] Database URL configured
- [ ] Connection pool settings optimized
- [ ] Backup strategy planned

### Security
- [ ] Environment variables not committed to Git
- [ ] `.env` files in `.gitignore`
- [ ] CORS restricted to specific origins
- [ ] HTTPS enabled on both frontend and backend
- [ ] SQL injection prevention (using SQLAlchemy ORM)
- [ ] XSS prevention (React escapes by default)

### Testing
- [ ] All API endpoints tested
- [ ] Authentication flow tested
- [ ] File upload functionality tested
- [ ] Proctoring system tested
- [ ] Candidate flow tested end-to-end
- [ ] Recruiter dashboard tested

## Deployment Steps

### 1. Backend (Render)
1. Create PostgreSQL database
2. Deploy web service
3. Configure environment variables
4. Test health endpoint
5. Monitor logs for errors

### 2. Frontend (Vercel)
1. Import GitHub repository
2. Configure build settings
3. Add environment variables
4. Deploy
5. Test live application

### 3. Post-Deployment
1. Update CORS in backend with frontend URL
2. Test all features on production
3. Set up monitoring/alerts
4. Document live URLs
5. Create admin/test accounts

## Monitoring

- [ ] Set up error tracking (Sentry, LogRocket, etc.)
- [ ] Configure uptime monitoring
- [ ] Set up database backup schedule
- [ ] Monitor API response times
- [ ] Track error rates

## Rollback Plan

1. Keep previous deployment accessible
2. Document rollback procedure
3. Have database backup ready
4. Test rollback in staging first

## Production URLs

- Frontend: `https://_______.vercel.app`
- Backend: `https://_______.onrender.com`
- Database: Render PostgreSQL

---

Last Updated: $(date)
