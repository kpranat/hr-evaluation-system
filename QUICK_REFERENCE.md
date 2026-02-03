# Quick Reference Guide - HR Evaluation System

## API Endpoints Quick Reference

### Authentication Endpoints

#### Candidate Login
```bash
POST /api/candidate/login
Content-Type: application/json

{
  "email": "candidate@example.com",
  "password": "password123"
}
```

#### Recruiter Login
```bash
POST /api/recruiter/login
Content-Type: application/json

{
  "email": "recruiter@example.com",
  "password": "password123"
}
```

#### Verify Token (Candidate/Recruiter)
```bash
GET /api/candidate/verify
# or
GET /api/recruiter/verify
Authorization: Bearer <your_jwt_token>
```

#### Bulk Upload Candidates
```bash
POST /api/recruiter/candidates/upload
Authorization: Bearer <recruiter_jwt_token>
Content-Type: multipart/form-data

# Form data:
file: [your_csv_or_excel_file]
```

---

## Blueprint Structure

### Quick Overview
```
CandidateAuth      → /api/candidate/*      → Candidate authentication
RecruiterAuth      → /api/recruiter/*      → Recruiter authentication  
RecruiterDashboard → /api/recruiter/*      → Recruiter operations
```

### Route Mapping
```
Blueprint            Route                           Method   Auth Required
─────────────────────────────────────────────────────────────────────────
CandidateAuth       /api/candidate/login            POST     No
CandidateAuth       /api/candidate/verify           GET      Yes (Candidate)
RecruiterAuth       /api/recruiter/login            POST     No
RecruiterAuth       /api/recruiter/verify           GET      Yes (Recruiter)
RecruiterDashboard  /api/recruiter/candidates/upload POST    Yes (Recruiter)
```

---

## File Locations

### Backend
```
app/CandidateAuth/route.py       → Candidate login & verify
app/RecruiterAuth/route.py       → Recruiter login & verify
app/RecruiterDashboard/route.py  → Bulk upload & dashboard features
app/models.py                    → Database models
app/__init__.py                  → Blueprint registration
```

### Frontend
```
src/lib/api.ts                              → API client functions
src/pages/admin/Candidates.tsx              → Candidates page
src/components/molecules/BulkUploadDialog.tsx → Upload dialog
```

---

## Common Tasks

### Add a New Route to RecruiterDashboard

1. Open `backend/app/RecruiterDashboard/route.py`
2. Add your route function:
```python
@RecruiterDashboard.route('/your-route', methods=['POST'])
def your_function():
    """
    YOUR ENDPOINT DESCRIPTION
    
    Purpose: What this endpoint does
    Authentication: Required/Not required
    Request: Expected request format
    Response: Expected response format
    Status Codes: List of status codes
    """
    # Your implementation
    pass
```

### Add Authentication to a Route

Use the helper function:
```python
from ..RecruiterDashboard.route import verify_recruiter_token

@YourBlueprint.route('/protected', methods=['GET'])
def protected_route():
    # Verify authentication
    is_valid, payload_or_error, status_code = verify_recruiter_token(request)
    
    if not is_valid:
        return jsonify({
            'success': False,
            'message': payload_or_error
        }), status_code
    
    # Your protected logic here
    pass
```

### Test an Endpoint with cURL

#### Login
```bash
curl -X POST http://localhost:5000/api/recruiter/login \
  -H "Content-Type: application/json" \
  -d '{"email":"recruiter@test.com","password":"password123"}'
```

#### With Authentication
```bash
curl -X GET http://localhost:5000/api/recruiter/verify \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### File Upload
```bash
curl -X POST http://localhost:5000/api/recruiter/candidates/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@sample_bulk_upload.csv"
```

---

## Database Operations

### Create Tables
```python
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
```

### Query Candidates
```python
from app.models import CandidateAuth

# Get all candidates
candidates = CandidateAuth.query.all()

# Find by email
candidate = CandidateAuth.query.filter_by(email='test@example.com').first()

# Check password
if candidate.check_password('plain_password'):
    print("Password correct!")
```

### Add New Candidate
```python
from app.models import CandidateAuth
from app.extensions import db

candidate = CandidateAuth(email='new@example.com')
candidate.set_password('password123')  # Automatically hashed
db.session.add(candidate)
db.session.commit()
```

---

## Environment Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
JWT_SECRET=your-secret-key-here
JWT_EXP_MINUTES=60

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## Status Codes Reference

```
200 OK                    → Success
201 Created              → Resource created
400 Bad Request          → Invalid input
401 Unauthorized         → Authentication required/failed
403 Forbidden            → Insufficient permissions
404 Not Found            → Resource not found
500 Internal Server Error → Server error
```

---

## JWT Token Structure

### Token Payload
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "type": "candidate|recruiter",
  "exp": 1234567890
}
```

### Token Usage
```javascript
// Store token
localStorage.setItem('recruiter_token', token);

// Use token in API calls
headers: {
  'Authorization': `Bearer ${token}`
}
```

---

## CSV File Format for Bulk Upload

```csv
email,password
candidate1@example.com,password123
candidate2@example.com,securepass456
candidate3@example.com,mypassword789
```

**Requirements:**
- Must have `email` and `password` columns
- Email must be unique
- Password will be automatically hashed
- Max file size: 10MB
- Formats: CSV, XLSX, XLS

---

## Error Response Format

All endpoints return errors in this format:
```json
{
  "success": false,
  "message": "Human-readable error message"
}
```

---

## Debugging Tips

### Check Blueprint Registration
```python
from app import create_app
app = create_app()
print(app.url_map)  # Shows all registered routes
```

### Test Database Connection
```python
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("✅ Database connected!")
    except Exception as e:
        print(f"❌ Database error: {e}")
```

### View All Routes
```python
from app import create_app
app = create_app()
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.methods} {rule.rule}")
```

---

## Security Checklist

- [ ] Passwords are hashed before storing
- [ ] JWT tokens expire after configured time
- [ ] Token type is verified (candidate vs recruiter)
- [ ] File uploads are validated (type, size)
- [ ] CORS is properly configured
- [ ] Environment variables are not committed to git
- [ ] SQL injection is prevented (using SQLAlchemy)
- [ ] Input validation on all endpoints

---

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "No token provided" | Missing Authorization header | Add `Authorization: Bearer <token>` |
| "Token has expired" | JWT token expired | Login again to get new token |
| "Invalid token type" | Wrong token type (candidate/recruiter) | Use correct token for endpoint |
| "Email and password are required" | Missing credentials | Include email and password in request |
| "Invalid email or password" | Wrong credentials | Check email and password |
| "No file provided" | Missing file in upload | Include file in form data |
| "Missing required columns" | CSV missing columns | Ensure CSV has email and password columns |

---

## Useful Commands

### Run Backend
```bash
cd backend
python run.py
```

### Run Frontend
```bash
cd frontend
npm run dev
```

### Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Install Frontend Dependencies
```bash
npm install
```

### Create Sample Data
```bash
python recreate_candidates.py
python recreate_recruiters.py
```

### View Database Records
```python
from app import create_app
from app.models import CandidateAuth, RecruiterAuth

app = create_app()
with app.app_context():
    print("Candidates:", CandidateAuth.query.count())
    print("Recruiters:", RecruiterAuth.query.count())
```

---

## Contact & Support

- Documentation: See `API_DOCUMENTATION.md`
- Architecture: See `ARCHITECTURE.md`
- Bulk Upload: See `BULK_UPLOAD_GUIDE.md`
- Refactoring: See `BLUEPRINT_REFACTORING.md`
