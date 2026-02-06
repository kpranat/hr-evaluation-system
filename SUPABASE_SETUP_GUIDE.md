# Supabase Integration Setup Guide

## Overview
The system now supports Supabase for storing coding questions in a cloud database. This allows for:
- **Question Bank**: Central repository of all available coding questions
- **Easy Migration**: One-time migration from local files to Supabase
- **Fast Access**: Questions loaded from Supabase instead of parsing files each time

## Prerequisites
1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Supabase Project**: Create a new project
3. **Python Package**: Already included in `requirements.txt`

## Setup Steps

### 1. Get Supabase Credentials
1. Go to your Supabase project dashboard
2. Click on **Settings** → **API**
3. Copy the following:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)

### 2. Configure Environment Variables
Add to your `.env` file:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### 3. Create Database Tables
Run the SQL schemas in your Supabase SQL Editor:

#### Question Bank Table (Required for migration)
```bash
# Open Supabase Dashboard → SQL Editor → New Query
# Copy and paste contents of: backend/supabase_question_bank_schema.sql
# Click "Run"
```

#### Active Problems Table (Optional - if using Supabase for active problems)
```bash
# Copy and paste contents of: backend/supabase_coding_problems_schema.sql
# Click "Run"
```

### 4. Migrate Questions to Supabase
Run the migration script to populate the question bank:

```bash
cd backend

# Dry run (preview what will be migrated)
python migrate_question_bank.py --dry-run

# Actual migration
python migrate_question_bank.py
```

**Expected Output:**
```
🚀 QUESTION BANK MIGRATION: Local Files → Supabase
======================================================================

✅ Supabase URL: https://xxxxx.supabase.co...
✅ Supabase Key: eyJhbGciOiJIUzI1NiIsInR5...
✅ Sample problems directory: D:\projects\...\CODING SAMPLE QUESTIONS\coding-problems

📂 Scanning local problem files...

📊 Found 131 problems in local files

📝 Migration Progress:

----------------------------------------------------------------------
[1/131] ✅ Successfully migrated: Two Sum (Arrays)
[2/131] ✅ Successfully migrated: Three Sum (Arrays)
...
======================================================================
📈 MIGRATION SUMMARY
======================================================================
Total questions scanned: 131
✅ Successfully migrated: 131
⏭️  Skipped (already exist): 0
❌ Failed: 0
======================================================================

🎉 Migration completed successfully!
   Your question bank is now populated in Supabase!
```

## How It Works

### Question Bank Flow
1. **Initial Setup**: Run migration script once to populate question bank
2. **Recruiter Action**: Click "Import from Bank" in Admin Dashboard
3. **Backend**: Fetches questions from Supabase `coding_question_bank` table
4. **Frontend**: Displays questions grouped by category
5. **Import**: Selected questions are copied to PostgreSQL `coding_problems` table

### Architecture
```
CODING SAMPLE QUESTIONS (local files)
         ↓
   [Migration Script]
         ↓
Supabase: coding_question_bank
         ↓
   [Import from Bank]
         ↓
PostgreSQL: coding_problems (active problems for candidates)
```

## Restored Files

### Services
- ✅ `backend/app/services/supabase_client.py` - Supabase client singleton
- ✅ `backend/app/services/coding_question_bank.py` - Question bank CRUD operations
- ✅ `backend/app/services/coding_problems_supabase.py` - Active problems CRUD operations

### Migration
- ✅ `backend/migrate_question_bank.py` - Migration script for populating question bank

### Schemas
- ✅ `backend/supabase_question_bank_schema.sql` - Question bank table schema
- ✅ `backend/supabase_coding_problems_schema.sql` - Active problems table schema

## Verifying Setup

### Test Supabase Connection
```python
# In Python console from backend directory
from app import create_app
from app.services.supabase_client import get_supabase

app = create_app()
with app.app_context():
    supabase = get_supabase()
    print("✅ Connected to Supabase!")
```

### Check Question Bank
```python
from app.services.coding_question_bank import CodingQuestionBankService

questions = CodingQuestionBankService.get_all_questions()
print(f"Found {len(questions)} questions in bank")
```

## Troubleshooting

### Error: "Could not find the table 'public.coding_question_bank'"
**Solution:** Run the schema SQL in Supabase SQL Editor:
```sql
-- Copy and run: backend/supabase_question_bank_schema.sql
```

### Error: "Supabase configuration missing"
**Solution:** Add SUPABASE_URL and SUPABASE_KEY to your `.env` file

### Error: "No problems to migrate"
**Solution:** Check that `CODING SAMPLE QUESTIONS/coding-problems/` folder exists with Python files

## Benefits
- 🚀 **Faster Loading**: Questions load instantly from Supabase
- 📦 **Centralized Storage**: One source of truth for all questions
- 🔄 **Easy Updates**: Update questions in Supabase without modifying files
- 🌐 **Cloud-based**: No need to deploy question files with application
- 📊 **Queryable**: Filter by category, difficulty, tags, etc.

## Alternative: Keep Using Local Files
If you prefer not to use Supabase, the system still works with local file scanning (original approach). Simply don't run the migration script and questions will be parsed from files on-demand.
