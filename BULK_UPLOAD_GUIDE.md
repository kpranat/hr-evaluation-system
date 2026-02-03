# Bulk Candidate Upload Feature

## Overview
The bulk candidate upload feature allows recruiters to add multiple candidates at once by uploading a CSV or Excel file. All passwords are automatically hashed using industry-standard werkzeug security before being stored in the database.

## Features
- ✅ Upload CSV, XLSX, or XLS files
- ✅ Automatic password hashing (werkzeug.security)
- ✅ Drag-and-drop file upload
- ✅ Progress tracking during upload
- ✅ Detailed upload results (created, updated, skipped)
- ✅ Error reporting for invalid entries
- ✅ File size validation (max 10MB)
- ✅ JWT authentication required

## How to Use

### 1. Prepare Your File

Create a CSV or Excel file with the following columns:

| email | password |
|-------|----------|
| john.doe@example.com | securePass123 |
| jane.smith@example.com | anotherPass456 |

**Required columns:**
- `email`: Candidate's email address (must be unique)
- `password`: Plain text password (will be hashed automatically)

**Sample file:** `sample_bulk_upload.csv`

### 2. Upload the File

1. Navigate to the **Candidates** page in the recruiter dashboard
2. Click the **"Add Candidates"** button (with upload icon)
3. Either:
   - **Drag and drop** your file into the upload area, or
   - Click **"browse"** to select a file from your computer
4. Click **"Upload Candidates"** to start the upload

### 3. View Results

After upload completes, you'll see:
- **Total candidates** processed
- **Created**: New candidates added
- **Updated**: Existing candidates with passwords updated
- **Skipped**: Invalid or incomplete entries
- **Errors**: Detailed error messages for problematic rows

## API Endpoint

### POST `/api/recruiter/candidates/upload`

**Authentication:** Bearer token (recruiter only)

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (CSV or Excel file)

**Response:**
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

## Security

### Password Hashing
- Passwords are hashed using `werkzeug.security.generate_password_hash()`
- Uses pbkdf2:sha256 algorithm by default
- Hashes are stored in the database, never plain text
- Password verification uses `check_password_hash()`

### Authentication
- Endpoint requires valid JWT token
- Only recruiter tokens are accepted
- Token must be included in Authorization header: `Bearer <token>`

## Installation

### Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `pandas`: For CSV/Excel file processing
- `openpyxl`: For Excel file support

### Frontend
No additional dependencies required. Uses existing shadcn/ui components.

## File Structure

### Backend
- `backend/app/RecruiterAuth/route.py` - Authentication endpoints (login, verify)
- `backend/app/RecruiterDashboard/route.py` - Dashboard endpoints (bulk upload, candidates management)
- `backend/app/models.py` - CandidateAuth model with password hashing

### Frontend
- `frontend/src/pages/admin/Candidates.tsx` - Main candidates page with upload button
- `frontend/src/components/molecules/BulkUploadDialog.tsx` - Upload dialog component
- `frontend/src/lib/api.ts` - API client with `uploadCandidates()` function

## Blueprint Architecture

The backend uses Flask blueprints for modular organization:

### RecruiterAuth Blueprint
**Purpose:** Handles recruiter authentication
- `/api/recruiter/login` - Recruiter login
- `/api/recruiter/verify` - Token verification

### RecruiterDashboard Blueprint
**Purpose:** Handles recruiter dashboard operations
- `/api/recruiter/candidates/upload` - Bulk candidate upload
- Future endpoints: candidate management, analytics, reporting

## Testing

### Sample File
Use the provided `sample_bulk_upload.csv` file to test the upload:

```csv
email,password
test.candidate1@example.com,password123
test.candidate2@example.com,securePass456
test.candidate3@example.com,myPass789
```

### Manual Testing Steps
1. Start the backend server: `python run.py`
2. Start the frontend dev server: `npm run dev`
3. Login as a recruiter
4. Navigate to Candidates page
5. Upload the sample CSV file
6. Verify candidates are created in the database

### Database Verification
```python
from app import create_app
from app.models import CandidateAuth

app = create_app()
with app.app_context():
    candidates = CandidateAuth.query.all()
    for c in candidates:
        print(f"Email: {c.email}, Hashed Password: {c.password[:20]}...")
```

## Error Handling

The upload process handles various error scenarios:

1. **Missing file**: Returns 400 error
2. **Invalid file type**: Only CSV, XLSX, XLS allowed
3. **File too large**: Maximum 10MB
4. **Missing columns**: Requires 'email' and 'password'
5. **Invalid email**: Skipped with error message
6. **Missing password**: Skipped with error message
7. **Database errors**: Rolled back with error message

## Limitations

- Maximum file size: 10MB
- Accepted formats: CSV, XLSX, XLS
- Required columns: email, password
- Email must be unique per candidate
- Requires recruiter authentication

## Future Enhancements

Potential improvements:
- [ ] Bulk candidate deletion
- [ ] Export candidates to CSV
- [ ] Email validation
- [ ] Password strength requirements
- [ ] Custom field mapping
- [ ] Template download
- [ ] Preview before upload
- [ ] Background processing for large files
