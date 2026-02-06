# Quick Setup Checklist: Coding Questions Supabase Migration

## Pre-Setup ✓

- [ ] Supabase account created
- [ ] Supabase project created
- [ ] SUPABASE_URL noted from project settings
- [ ] SUPABASE_KEY (anon key) noted from project settings

## Setup Steps

### 1. Configure Environment
```bash
# Edit backend/.env file and add:
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```
- [ ] Environment variables added

### 2. Create Supabase Table
1. Open Supabase Dashboard → SQL Editor
2. Copy content from `backend/supabase_coding_problems_schema.sql`
3. Paste and run in SQL Editor
- [ ] SQL schema executed
- [ ] Table created (verify in Table Editor)

### 3. Migrate Existing Data (if applicable)
```bash
cd backend
# First, do a dry run
python migrate_coding_to_supabase.py --dry-run

# Then actual migration
python migrate_coding_to_supabase.py
```
- [ ] Dry run completed
- [ ] Migration executed
- [ ] Data verified in Supabase

### 4. Start Backend
```bash
cd backend
python run.py
```
- [ ] Backend started without errors

## Verification Tests

### Test 1: Recruiter Can View Problems
```bash
# Login and get token, then:
curl http://localhost:5000/api/code/admin/problems \
  -H "Authorization: Bearer YOUR_TOKEN"
```
- [ ] Problems returned from Supabase

### Test 2: Recruiter Can Create Problem
```bash
curl -X POST http://localhost:5000/api/code/admin/problems \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Problem",
    "description": "Test",
    "difficulty": "easy",
    "test_cases": [{"input": "1", "expected_output": "1", "is_hidden": false}]
  }'
```
- [ ] Problem created in Supabase

### Test 3: Candidate Can View Problems
```bash
curl http://localhost:5000/api/code/problems \
  -H "Authorization: Bearer CANDIDATE_TOKEN"
```
- [ ] Problems returned to candidate

### Test 4: Frontend Works
- [ ] Recruiter dashboard loads
- [ ] Coding Management page shows problems
- [ ] Candidate coding test page loads
- [ ] Problems display correctly

## Files Created/Modified

✅ Created:
- `backend/app/services/supabase_client.py`
- `backend/app/services/coding_problems_supabase.py`
- `backend/supabase_coding_problems_schema.sql`
- `backend/migrate_coding_to_supabase.py`
- `SUPABASE_CODING_MIGRATION_GUIDE.md`
- `SUPABASE_CODING_QUICK_SETUP.md` (this file)

✅ Modified:
- `backend/app/CodeExecution/route.py`

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Supabase credentials not configured" | Add SUPABASE_URL and SUPABASE_KEY to .env |
| "Table not found" | Run SQL schema in Supabase SQL Editor |
| "No problems returned" | Check Supabase Table Editor for data |
| Migration fails | Ensure backend is not running during migration |

## Success Indicators ✓

- [ ] ✅ Supabase table exists and has data
- [ ] ✅ Backend starts without errors
- [ ] ✅ Recruiter can view problems
- [ ] ✅ Recruiter can create problems
- [ ] ✅ Recruiter can import problems
- [ ] ✅ Candidate can view problems
- [ ] ✅ Frontend displays problems correctly
- [ ] ✅ No console errors in browser

## What's Next?

After successful setup:
1. Add categories/tags to your problems
2. Test problem submission workflow
3. Monitor Supabase usage in dashboard
4. Consider backing up your Supabase data

## Rollback (if needed)

```bash
git checkout HEAD -- backend/app/CodeExecution/route.py
python run.py
```

---

**Total Setup Time:** ~15-20 minutes
**Difficulty:** Easy
**Impact:** Problems now served from Supabase

✅ Setup Complete! Enjoy your Supabase-powered coding platform!
