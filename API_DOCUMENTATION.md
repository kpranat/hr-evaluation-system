# API Routes Documentation

This document provides a comprehensive overview of all API endpoints in the HR Evaluation System.

## Table of Contents
- [Candidate Authentication](#candidate-authentication)
- [Recruiter Authentication](#recruiter-authentication)
- [Recruiter Dashboard](#recruiter-dashboard)

---

## Candidate Authentication

**Blueprint:** `CandidateAuth`  
**URL Prefix:** `/api/candidate`

### POST `/api/candidate/login`

**Purpose:** Authenticates candidate credentials and returns JWT token for assessment access.

**Authentication:** Not required (public endpoint)

**Request:**
```json
{
  "email": "candidate@example.com",
  "password": "plain_text_password"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "JWT_TOKEN_STRING",
  "user": {
    "id": 1,
    "email": "candidate@example.com"
  }
}
```

**Error Response (400/401):**
```json
{
  "success": false,
  "message": "Error message"
}
```

**Status Codes:**
- `200` - Login successful
- `400` - Missing email or password
- `401` - Invalid credentials
- `500` - Server error

**Processing Logic:**
1. Validate request contains email and password
2. Query database for candidate by email
3. Verify password using check_password() method
4. Generate JWT token with candidate details
5. Return token and user info

---

### GET `/api/candidate/verify`

**Purpose:** Verifies the validity of a candidate JWT token and returns user information.

**Authentication:** Required (JWT Bearer token)

**Request Headers:**
```
Authorization: Bearer JWT_TOKEN_STRING
```

**Success Response (200):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "email": "candidate@example.com"
  }
}
```

**Error Response (401):**
```json
{
  "valid": false,
  "message": "Error message"
}
```

**Status Codes:**
- `200` - Token is valid
- `401` - Missing token, invalid token, expired token, or wrong token type
- `500` - Server error

**Use Cases:**
- Session validation during assessment
- Protected route authentication
- Assessment continuation after refresh

---

## Recruiter Authentication

**Blueprint:** `RecruiterAuth`  
**URL Prefix:** `/api/recruiter`

### POST `/api/recruiter/login`

**Purpose:** Authenticates recruiter credentials and returns JWT token for subsequent requests.

**Authentication:** Not required (public endpoint)

**Request:**
```json
{
  "email": "recruiter@example.com",
  "password": "plain_text_password"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "JWT_TOKEN_STRING",
  "user": {
    "id": 1,
    "email": "recruiter@example.com"
  }
}
```

**Error Response (400/401):**
```json
{
  "success": false,
  "message": "Error message"
}
```

**Status Codes:**
- `200` - Login successful
- `400` - Missing email or password
- `401` - Invalid credentials
- `500` - Server error

**Token Details:**
- Algorithm: HS256
- Expiration: Configured in Config.JWT_EXP_MINUTES
- Payload includes: user_id, email, type='recruiter', exp

---

### GET `/api/recruiter/verify`

**Purpose:** Verifies the validity of a recruiter JWT token and returns user information.

**Authentication:** Required (JWT Bearer token)

**Request Headers:**
```
Authorization: Bearer JWT_TOKEN_STRING
```

**Success Response (200):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "email": "recruiter@example.com",
    "type": "recruiter"
  }
}
```

**Error Response (401):**
```json
{
  "valid": false,
  "message": "Error message"
}
```

**Status Codes:**
- `200` - Token is valid
- `401` - Missing token, invalid token, expired token, or wrong token type
- `500` - Server error

**Use Cases:**
- Session validation on app load
- Protected route authentication
- Token refresh validation

---

## Recruiter Dashboard

**Blueprint:** `RecruiterDashboard`  
**URL Prefix:** `/api/recruiter`

### POST `/api/recruiter/candidates/upload`

**Purpose:** Handles bulk upload of candidates from CSV or Excel files. Automatically hashes passwords before storing in database.

**Authentication:** Required (JWT Bearer token - recruiter only)

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (CSV/Excel file)
- File must contain columns: `email`, `password`

**Request Headers:**
```
Authorization: Bearer JWT_TOKEN_STRING
```

**Supported File Formats:**
- CSV (.csv)
- Excel (.xlsx, .xls)

**File Constraints:**
- Maximum size: 10MB
- Required columns: email, password

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully processed 10 candidates",
  "results": {
    "total": 10,
    "created": 8,
    "updated": 2,
    "skipped": 0,
    "errors": []
  }
}
```

**Error Response (400/401/403/500):**
```json
{
  "success": false,
  "message": "Error message",
  "results": {
    "total": 10,
    "created": 5,
    "updated": 0,
    "skipped": 5,
    "errors": [
      "Row 3: Missing email",
      "Row 7: Missing password"
    ]
  }
}
```

**Status Codes:**
- `200` - Upload successful (even with partial errors)
- `400` - Bad request (missing file, invalid format, missing columns)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (not a recruiter token)
- `500` - Server error (database error)

**Processing Logic:**
For each row in the file:
1. If email exists: Update password (hashed)
2. If email doesn't exist: Create new candidate (password hashed)
3. If email/password missing: Skip row and log error

**Security:**
- Passwords are hashed using `werkzeug.security.generate_password_hash()`
- Uses pbkdf2:sha256 algorithm
- No plain text passwords are stored

**Required File Format:**
```csv
email,password
john.doe@example.com,securePass123
jane.smith@example.com,anotherPass456
```

---

## Common Response Codes

### Success Codes
- `200 OK` - Request successful
- `201 Created` - Resource created successfully

### Client Error Codes
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found

### Server Error Codes
- `500 Internal Server Error` - Server-side error

---

## Authentication

### JWT Token Structure

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

**Token Payload:**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "type": "candidate|recruiter",
  "exp": 1234567890
}
```

**Token Types:**
- `candidate` - For candidate users
- `recruiter` - For recruiter users

### Token Expiration

Tokens expire after a configured duration (default: Config.JWT_EXP_MINUTES).
Use the `/verify` endpoint to check token validity.

---

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "success": false,
  "message": "Human-readable error message",
  "error": "Optional error code or details"
}
```

### Common Error Messages

**Authentication Errors:**
- "No token provided"
- "Invalid token"
- "Token has expired"
- "Invalid token type"
- "Authentication required"
- "Unauthorized: Recruiter access required"

**Validation Errors:**
- "Email and password are required"
- "Invalid email or password"
- "No file provided"
- "No file selected"
- "Invalid file type"
- "Missing required columns"

**Server Errors:**
- "Database error: [details]"
- "An error occurred: [details]"

---

## Blueprint Architecture

The backend is organized using Flask blueprints for modularity:

### CandidateAuth Blueprint
- **Purpose:** Candidate authentication
- **Prefix:** `/api/candidate`
- **Routes:** login, verify

### RecruiterAuth Blueprint
- **Purpose:** Recruiter authentication
- **Prefix:** `/api/recruiter`
- **Routes:** login, verify

### RecruiterDashboard Blueprint
- **Purpose:** Recruiter dashboard operations
- **Prefix:** `/api/recruiter`
- **Routes:** candidates/upload, (future: analytics, reporting)

This separation ensures:
- Clear separation of concerns
- Easy to maintain and extend
- Modular code organization
- Independent testing of each module

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production:
- Login endpoints: 5 requests per minute
- Upload endpoints: 10 requests per hour
- Verify endpoints: 100 requests per minute

---

## CORS Configuration

CORS is enabled for all `/api/*` routes with:
- Allowed Origins: `*` (configure for production)
- Allowed Methods: GET, POST, PUT, DELETE, OPTIONS
- Allowed Headers: Content-Type, Authorization

---

## Database Models

### CandidateAuth
```python
{
  "id": Integer (Primary Key),
  "email": String(100) (Unique),
  "password": String(255) (Hashed)
}
```

### RecruiterAuth
```python
{
  "id": Integer (Primary Key),
  "email": String(100) (Unique),
  "password": String(255) (Hashed)
}
```

Both models include:
- `set_password(password)` - Hash and set password
- `check_password(password)` - Verify password
- `to_dict()` - Convert to JSON-serializable dict

---

## Future Endpoints

### Recruiter Dashboard (Planned)
- `GET /api/recruiter/candidates` - List all candidates
- `GET /api/recruiter/candidates/<id>` - Get candidate details
- `DELETE /api/recruiter/candidates/<id>` - Delete candidate
- `GET /api/recruiter/analytics` - Dashboard analytics
- `PUT /api/recruiter/settings` - Update settings

### Candidate Assessment (Planned)
- `GET /api/candidate/assessment` - Get assessment questions
- `POST /api/candidate/assessment/submit` - Submit assessment
- `GET /api/candidate/results` - Get assessment results
