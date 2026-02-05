# Coding Round - Quick Testing Guide

## Prerequisites
✅ Database migration completed (`python backend/create_coding_tables.py`)
✅ Backend server running (`python backend/run.py`)
✅ Frontend dev server running (`cd frontend && npm run dev`)

## Testing the Complete Workflow

### 1. Database Verification
Check that all tables exist:
```sql
-- Connect to your Supabase PostgreSQL database
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('coding_problems', 'coding_submissions', 'coding_configuration');

-- Verify sample problem exists
SELECT * FROM coding_problems WHERE problem_id = 1;

-- Check default configuration
SELECT * FROM coding_configuration;
```

### 2. Backend API Testing

#### Test Configuration Endpoint
```bash
curl -X GET http://localhost:5000/api/code/config \
  -H "Authorization: Bearer YOUR_CANDIDATE_TOKEN"
```
Expected Response:
```json
{
  "problems_count": 3,
  "time_limit_minutes": 60,
  "allowed_languages": ["python", "javascript", "java", "cpp"]
}
```

#### Test Problems List
```bash
curl -X GET http://localhost:5000/api/code/problems \
  -H "Authorization: Bearer YOUR_CANDIDATE_TOKEN"
```
Expected Response:
```json
{
  "problems": [
    {
      "problem_id": 1,
      "title": "Two Sum",
      "difficulty": "easy",
      "status": "not_attempted"
    }
  ]
}
```

#### Test Problem Details
```bash
curl -X GET http://localhost:5000/api/code/problems/1 \
  -H "Authorization: Bearer YOUR_CANDIDATE_TOKEN"
```

#### Test Code Execution
```bash
curl -X POST http://localhost:5000/api/code/execute \
  -H "Authorization: Bearer YOUR_CANDIDATE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": 1,
    "code": "def twoSum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]",
    "language": "python"
  }'
```

#### Test Code Submission
```bash
curl -X POST http://localhost:5000/api/code/submit \
  -H "Authorization: Bearer YOUR_CANDIDATE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": 1,
    "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i",
    "language": "python"
  }'
```

#### Test Round Completion
```bash
curl -X POST http://localhost:5000/api/code/complete \
  -H "Authorization: Bearer YOUR_CANDIDATE_TOKEN"
```

### 3. Frontend UI Testing

#### Step-by-Step Candidate Journey

1. **Login as Candidate**
   - Navigate to http://localhost:5173/candidate/login
   - Login with test candidate credentials

2. **Complete Prerequisites**
   - Complete MCQ round
   - Complete Psychometric round
   - Complete Technical round
   - Complete Text-Based round

3. **Navigate to Coding Round**
   - Go to Candidate Home: http://localhost:5173/candidate/home
   - Verify coding round card shows in workflow
   - Card should show as "locked" until text-based is completed
   - Once text-based is done, click "Start" on coding round

4. **Test Coding Interface**
   - Verify URL is: http://localhost:5173/candidate/coding-test
   - Check timer starts countdown (default: 60 minutes)
   - Verify problem list loads in left sidebar
   - Click on "Two Sum" problem

5. **Test Code Editor**
   - Verify Monaco editor loads with Python starter code
   - Switch language to JavaScript - verify starter code changes
   - Switch to Java - verify starter code changes
   - Switch to C++ - verify starter code changes
   - Return to Python

6. **Test Code Execution (Run)**
   - Write a simple solution:
   ```python
   def twoSum(nums, target):
       for i in range(len(nums)):
           for j in range(i+1, len(nums)):
               if nums[i] + nums[j] == target:
                   return [i, j]
   ```
   - Click "Run" button
   - Verify test results appear in right panel
   - Check each test case shows pass/fail status
   - Verify stdout/stderr output displays

7. **Test Code Submission**
   - Write correct solution:
   ```python
   def twoSum(nums, target):
       seen = {}
       for i, num in enumerate(nums):
           complement = target - num
           if complement in seen:
               return [seen[complement], i]
           seen[num] = i
   ```
   - Click "Submit" button
   - Verify success message appears
   - Check problem status changes to "accepted" (✓)
   - Verify submission appears in "Previous Submissions" panel

8. **Test Submission History**
   - Click "View Submissions" button
   - Verify list shows all previous submissions
   - Check submission details (code, language, status, timestamp)

9. **Complete the Round**
   - Solve all problems (or skip if testing)
   - Click "Complete Round" button at top
   - Verify redirect to candidate home
   - Check that coding round card shows "Completed ✓"

10. **Verify Database Updates**
    ```sql
    -- Check coding_completed flag
    SELECT email, coding_completed, coding_completed_at 
    FROM candidate_auth 
    WHERE email = 'test@example.com';

    -- Check submissions
    SELECT * FROM coding_submissions 
    WHERE candidate_id = (SELECT candidate_id FROM candidate_auth WHERE email = 'test@example.com');
    ```

### 4. Edge Case Testing

#### Test Timer Expiration
1. Manually set time limit to 1 minute in configuration
2. Wait for timer to expire
3. Verify UI shows warning at 5 minutes remaining
4. Verify automatic submission when timer hits 0

#### Test Error Handling
1. **Syntax Error**:
   - Write invalid Python code: `def twoSum(nums, target`
   - Click "Run"
   - Verify error message displays in console

2. **Runtime Error**:
   - Write code that crashes: `return nums[999]`
   - Click "Run"
   - Verify runtime error displays

3. **Wrong Answer**:
   - Write incorrect logic: `return [0, 1]` always
   - Click "Submit"
   - Verify status shows "wrong_answer"

4. **Timeout**:
   - Write infinite loop: `while True: pass`
   - Click "Run"
   - Verify timeout error after 5 seconds

#### Test Language Switching
1. Write code in Python
2. Switch to JavaScript - verify code doesn't change
3. Write different code in JavaScript
4. Switch back to Python - verify original Python code persists
5. Submit both versions separately

#### Test Problem Navigation
1. Open Problem 1, write code
2. Navigate to Problem 2
3. Return to Problem 1
4. Verify code is still there (local state preserved)

### 5. Performance Testing
- Load 10+ problems - verify UI remains responsive
- Execute code multiple times rapidly - verify queue handling
- Submit code while timer is running - verify no conflicts

### 6. Security Testing
- Try accessing `/candidate/coding-test` without token - verify redirect to login
- Try accessing coding round before completing text-based - verify lock/redirect
- Try submitting with invalid problem_id - verify error handling
- Try executing malicious code (file I/O) - verify sandbox restrictions

## Expected Behavior Summary

### Status Flow:
1. Initial: `not_attempted` (○ gray circle)
2. After first run: `attempted` (⚠ orange warning)
3. After correct submit: `accepted` (✓ green checkmark)

### Timer Behavior:
- Starts automatically on page load
- Shows warning when < 5 minutes remaining
- Auto-submits when reaches 0
- Format: MM:SS

### Submission Outcomes:
- `accepted`: All test cases passed
- `wrong_answer`: Some test cases failed
- `runtime_error`: Code crashed during execution
- `time_limit_exceeded`: Execution took too long

## Common Issues & Fixes

### Issue: Problems don't load
- **Fix**: Check backend API is running on port 5000
- **Fix**: Verify candidate token is valid
- **Fix**: Check PostgreSQL connection in backend

### Issue: Code execution fails
- **Fix**: Verify Piston API is accessible (https://emkc.org/api/v2/piston/execute)
- **Fix**: Check network/firewall settings
- **Fix**: Test Piston API directly with curl

### Issue: Monaco editor doesn't load
- **Fix**: Check `@monaco-editor/react` package is installed
- **Fix**: Verify frontend build has no errors
- **Fix**: Check browser console for errors

### Issue: Timer doesn't start
- **Fix**: Verify config API returns valid time_limit_minutes
- **Fix**: Check useEffect hook is running
- **Fix**: Inspect React state in DevTools

### Issue: Submissions not saving
- **Fix**: Check database connection
- **Fix**: Verify candidate_id is valid
- **Fix**: Check PostgreSQL logs for errors

## Success Criteria
✅ All API endpoints return 200 status
✅ Problems load and display correctly
✅ Code editor works with all 4 languages
✅ Run button executes code and shows results
✅ Submit button saves to database
✅ Timer counts down correctly
✅ Status indicators update properly
✅ Submission history displays
✅ Round completion marks candidate as done
✅ Workflow progresses correctly from text-based to coding

## Need Help?
- Check `CODING_ROUND_INTEGRATION.md` for architecture details
- Review `backend/app/CodeExecution/route.py` for API documentation
- Inspect browser DevTools Console for frontend errors
- Check Flask terminal for backend errors
- Query PostgreSQL database directly to verify data
