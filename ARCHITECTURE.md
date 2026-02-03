# HR Evaluation System - Backend Architecture

## Blueprint Organization

```
┌─────────────────────────────────────────────────────────────────┐
│                        Flask Application                         │
│                        (app/__init__.py)                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │    Blueprint Registration    │
                └──────────────┬──────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐      ┌───────────────┐     ┌──────────────────┐
│ CandidateAuth │      │ RecruiterAuth │     │RecruiterDashboard│
│   Blueprint   │      │   Blueprint   │     │    Blueprint     │
├───────────────┤      ├───────────────┤     ├──────────────────┤
│ Prefix:       │      │ Prefix:       │     │ Prefix:          │
│ /api/candidate│      │ /api/recruiter│     │ /api/recruiter   │
├───────────────┤      ├───────────────┤     ├──────────────────┤
│ Routes:       │      │ Routes:       │     │ Routes:          │
│               │      │               │     │                  │
│ POST /login   │      │ POST /login   │     │ POST /candidates │
│ ↓ Authenticate│      │ ↓ Authenticate│     │      /upload     │
│   candidate   │      │   recruiter   │     │ ↓ Bulk upload    │
│               │      │               │     │   candidates     │
│ GET /verify   │      │ GET /verify   │     │                  │
│ ↓ Verify      │      │ ↓ Verify      │     │ Future:          │
│   candidate   │      │   recruiter   │     │ - List candidates│
│   token       │      │   token       │     │ - Analytics      │
│               │      │               │     │ - Reporting      │
└───────────────┘      └───────────────┘     └──────────────────┘
        │                      │                      │
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Database Models                          │
│                         (app/models.py)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CandidateAuth Model              RecruiterAuth Model           │
│  ├─ id: Integer                   ├─ id: Integer                │
│  ├─ email: String(100)            ├─ email: String(100)         │
│  ├─ password: String(255)         ├─ password: String(255)      │
│  ├─ set_password(password)        ├─ set_password(password)     │
│  ├─ check_password(password)      ├─ check_password(password)   │
│  └─ to_dict()                     └─ to_dict()                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### Candidate Login Flow
```
1. Client Request
   POST /api/candidate/login
   { "email": "...", "password": "..." }
   
2. CandidateAuth Blueprint
   ├─ Validate input
   ├─ Query CandidateAuth model
   ├─ Check password (hashed)
   └─ Generate JWT token
   
3. Response
   { "success": true, "token": "...", "user": {...} }
```

### Recruiter Login Flow
```
1. Client Request
   POST /api/recruiter/login
   { "email": "...", "password": "..." }
   
2. RecruiterAuth Blueprint
   ├─ Validate input
   ├─ Query RecruiterAuth model
   ├─ Check password (hashed)
   └─ Generate JWT token
   
3. Response
   { "success": true, "token": "...", "user": {...} }
```

### Bulk Upload Flow
```
1. Client Request
   POST /api/recruiter/candidates/upload
   Headers: { "Authorization": "Bearer <token>" }
   Body: multipart/form-data with file
   
2. RecruiterDashboard Blueprint
   ├─ Verify recruiter token
   ├─ Validate file format
   ├─ Read CSV/Excel file
   ├─ Process each row:
   │  ├─ Check if candidate exists
   │  ├─ Hash password
   │  └─ Create/Update candidate
   └─ Commit to database
   
3. Response
   {
     "success": true,
     "results": {
       "total": 10,
       "created": 8,
       "updated": 2,
       "skipped": 0,
       "errors": []
     }
   }
```

## Authentication Flow

```
┌────────────┐                 ┌────────────┐
│   Client   │                 │   Server   │
└──────┬─────┘                 └─────┬──────┘
       │                             │
       │  POST /api/.../login        │
       │  (email, password)          │
       ├────────────────────────────►│
       │                             │
       │                        ┌────▼────┐
       │                        │ Verify  │
       │                        │Password │
       │                        └────┬────┘
       │                             │
       │                        ┌────▼────┐
       │                        │Generate │
       │                        │JWT Token│
       │                        └────┬────┘
       │                             │
       │  Response with token        │
       │◄────────────────────────────┤
       │                             │
       │  Store token locally        │
       ├─────────────────────────────┤
       │                             │
       │  Future requests            │
       │  Header: Bearer <token>     │
       ├────────────────────────────►│
       │                             │
       │                        ┌────▼────┐
       │                        │ Verify  │
       │                        │  Token  │
       │                        └────┬────┘
       │                             │
       │  Protected resource         │
       │◄────────────────────────────┤
       │                             │
```

## File Structure

```
hr-evaluation-system/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py              ← App initialization
│   │   ├── config.py                ← Configuration
│   │   ├── extensions.py            ← Flask extensions (db, etc.)
│   │   ├── models.py                ← Database models
│   │   │
│   │   ├── CandidateAuth/           ← Candidate authentication
│   │   │   ├── __init__.py          ← Blueprint registration
│   │   │   └── route.py             ← Routes (login, verify)
│   │   │
│   │   ├── RecruiterAuth/           ← Recruiter authentication
│   │   │   ├── __init__.py          ← Blueprint registration
│   │   │   └── route.py             ← Routes (login, verify)
│   │   │
│   │   └── RecruiterDashboard/      ← Recruiter dashboard
│   │       ├── __init__.py          ← Blueprint registration
│   │       └── route.py             ← Routes (bulk upload, etc.)
│   │
│   ├── requirements.txt             ← Python dependencies
│   ├── run.py                       ← Application entry point
│   └── .env                         ← Environment variables
│
└── frontend/
    └── src/
        ├── lib/
        │   └── api.ts               ← API client functions
        │
        ├── pages/
        │   └── admin/
        │       └── Candidates.tsx   ← Candidates page
        │
        └── components/
            └── molecules/
                └── BulkUploadDialog.tsx  ← Upload dialog
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Security Layers                       │
└─────────────────────────────────────────────────────────────┘

1. Password Security
   ├─ Hash Algorithm: pbkdf2:sha256
   ├─ Library: werkzeug.security
   ├─ Function: generate_password_hash()
   └─ Verification: check_password_hash()

2. Token Security
   ├─ Algorithm: HS256
   ├─ Library: PyJWT
   ├─ Expiration: Configurable (JWT_EXP_MINUTES)
   └─ Payload: user_id, email, type, exp

3. Authentication Middleware
   ├─ Helper: verify_recruiter_token()
   ├─ Checks: Token presence, validity, expiration
   └─ Type verification: candidate vs recruiter

4. CORS Protection
   ├─ Enabled for: /api/*
   ├─ Allowed origins: Configurable
   └─ Allowed methods: GET, POST, PUT, DELETE, OPTIONS
```

## Data Flow Diagram

```
Frontend (React)                Backend (Flask)              Database (PostgreSQL)
     │                               │                              │
     │  1. Upload File               │                              │
     ├──────────────────────────────►│                              │
     │                               │                              │
     │                          2. Verify Token                     │
     │                               ├──────────────────────────────┤
     │                               │  (JWT validation)            │
     │                               │                              │
     │                          3. Read File                        │
     │                               │  (pandas)                    │
     │                               │                              │
     │                          4. Process Rows                     │
     │                               │  (iterate DataFrame)         │
     │                               │                              │
     │                          5. Hash Passwords                   │
     │                               │  (werkzeug.security)         │
     │                               │                              │
     │                          6. Save to DB                       │
     │                               ├─────────────────────────────►│
     │                               │  (SQLAlchemy commit)         │
     │                               │                              │
     │  7. Return Results            │                              │
     │◄──────────────────────────────┤                              │
     │                               │                              │
```

## Blueprint Responsibilities

### CandidateAuth Blueprint
**Responsibility:** Manage candidate authentication lifecycle

**Operations:**
- Authenticate candidate credentials
- Issue JWT tokens for candidates
- Verify candidate tokens

**Security:**
- Password hashing on login
- Token generation with type='candidate'
- Token validation

### RecruiterAuth Blueprint
**Responsibility:** Manage recruiter authentication lifecycle

**Operations:**
- Authenticate recruiter credentials
- Issue JWT tokens for recruiters
- Verify recruiter tokens

**Security:**
- Password hashing on login
- Token generation with type='recruiter'
- Token validation

### RecruiterDashboard Blueprint
**Responsibility:** Manage recruiter dashboard operations

**Operations:**
- Bulk candidate upload
- Candidate management (future)
- Analytics and reporting (future)

**Security:**
- Token verification (recruiter-only)
- File validation
- Database transaction management

## Advantages of Blueprint Architecture

✅ **Modularity**
   - Each blueprint is self-contained
   - Easy to add/remove features
   - Independent testing

✅ **Scalability**
   - Can split into microservices later
   - Easy to add new blueprints
   - Clear boundaries

✅ **Maintainability**
   - Clear code organization
   - Easy to locate functionality
   - Comprehensive documentation

✅ **Security**
   - Isolated authentication logic
   - Clear permission boundaries
   - Centralized token validation

✅ **Team Collaboration**
   - Different teams can work on different blueprints
   - Minimal merge conflicts
   - Clear ownership
