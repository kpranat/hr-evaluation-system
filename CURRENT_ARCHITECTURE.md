# Current Architecture - PostgreSQL Only

## Overview
The system uses **PostgreSQL only** for storing coding problems. No Supabase integration.

## How It Works

### Database Tables (PostgreSQL)
- `coding_problems` - Active problems assigned to candidates
- `coding_submissions` - Candidate submissions and results
- Other tables for MCQ, psychometric, candidates, etc.

### Question Bank System
**Questions are stored in local files**, not in a database table.

#### File Location
```
CODING SAMPLE QUESTIONS/
  coding-problems/
    Arrays/
      two-sum.py
      three-sum.py
      ...
    Dynamic Programming/
      ...
    Linked Lists/
      ...
```

#### Import Workflow
1. **Recruiter clicks "Import from Bank"** in Admin Dashboard
2. **Backend scans files** from `CODING SAMPLE QUESTIONS` folder in real-time
3. **Frontend displays** all available problems grouped by category
4. **Recruiter selects** problems to import
5. **Backend parses** selected Python files using `problem_parser.py`
6. **Backend inserts** parsed problems into PostgreSQL `coding_problems` table

### Key Backend Files
- `backend/app/CodeExecution/route.py` - API endpoints
  - `GET /admin/import/scan` - Scans local files and returns list
  - `POST /admin/import/batch` - Parses and imports selected files to DB
- `backend/app/CodeExecution/problem_parser.py` - Parses Python problem files
- `backend/app/models.py` - `CodingProblem` model for PostgreSQL

### Key Frontend Files
- `frontend/src/pages/admin/CodingManagement.tsx` - Import UI

## API Endpoints

### Scan Sample Problems
```http
GET /api/code/admin/import/scan
Authorization: Bearer {recruiter_token}

Response:
{
  "success": true,
  "problems": [
    {
      "file_path": "path/to/two-sum.py",
      "title": "Two Sum",
      "category": "Arrays",
      "difficulty": "easy",
      "test_cases_count": 3,
      "description_preview": "Given an array..."
    }
  ],
  "categories": {
    "Arrays": [...],
    "Dynamic Programming": [...]
  },
  "total": 131
}
```

### Import Selected Problems
```http
POST /api/code/admin/import/batch
Authorization: Bearer {recruiter_token}
Content-Type: application/json

{
  "file_paths": [
    "path/to/two-sum.py",
    "path/to/three-sum.py"
  ]
}

Response:
{
  "success": true,
  "imported": 2,
  "failed": 0,
  "errors": [],
  "message": "Imported 2 out of 2 problems"
}
```

## Problem File Format
```python
'''
Problem Title
Problem description explaining the task.

Input: [example input]
Output: expected output
=========================================
Approach explanation
Time Complexity: O(N)
'''
def solution_function(params):
    # Implementation
    pass

# Testing #
print(solution_function(test_input))  # Correct result => expected_output
```

## No Supabase
- All coding problems are in **PostgreSQL**
- Question bank is **file-based** (no database table)
- Scanning happens **on-demand** when recruiter clicks import
- No migration scripts needed

## Running the System
```bash
# Backend
cd backend
python run.py

# Frontend
cd frontend
npm run dev
```

## Adding New Sample Questions
1. Create a `.py` file in `CODING SAMPLE QUESTIONS/coding-problems/{category}/`
2. Follow the problem file format above
3. It will automatically appear when recruiter clicks "Import from Bank"
