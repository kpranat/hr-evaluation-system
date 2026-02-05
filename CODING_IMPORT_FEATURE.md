# Coding Problem Import Feature

## Overview
Added functionality to import coding problems from the "CODING SAMPLE QUESTIONS" folder directly into the database, giving recruiters the option to:
1. **Import from Sample Bank** - Select and import problems from existing Python files
2. **Add Manually** - Create problems from scratch (existing feature)

## Files Created/Modified

### Backend

#### New Files:
1. **`backend/app/CodeExecution/problem_parser.py`**
   - Parses Python problem files to extract:
     - Problem title (from docstring first line)
     - Problem description
     - Function signature and parameters
     - Test cases (input/expected output)
     - Category (from folder name)
     - Difficulty (auto-detected)
   - Generates starter code template
   - Successfully scans **131 problems** from sample folder

#### Modified Files:
2. **`backend/app/CodeExecution/route.py`**
   - Added `import os` for file path handling
   - **New Endpoint**: `GET /api/code/admin/import/scan`
     - Scans sample problems folder
     - Returns all problems grouped by category
     - Requires recruiter authentication
   - **New Endpoint**: `POST /api/code/admin/import/batch`
     - Imports selected problems into database
     - Checks for duplicates by title
     - Returns success/failure counts with error messages
     - Requires recruiter authentication

### Frontend

#### Modified Files:
3. **`frontend/src/pages/admin/CodingManagement.tsx`**
   - Added new imports: `Checkbox`, `Tabs`, `ScrollArea`, `Upload`, `Loader2` icons
   - Added `SampleProblem` interface
   - New state variables:
     - `sampleProblems` - List of scanned problems
     - `categorizedProblems` - Problems grouped by category
     - `selectedProblems` - Set of selected problem file paths
     - `loadingSamples` - Loading state for scan
     - `importing` - Loading state for import
     - `isImportDialogOpen` - Import dialog visibility
   - New functions:
     - `fetchSampleProblems()` - Calls scan endpoint
     - `handleToggleProblem()` - Toggle individual problem selection
     - `handleToggleCategory()` - Select/deselect all problems in a category
     - `handleImportSelected()` - Import selected problems
   - New UI:
     - "Import from Bank" button in header
     - Import dialog with tabs for each category
     - Checkbox list of problems with title, difficulty, description preview
     - "Select All" / "Deselect All" buttons per category
     - Selected count display
     - "Import Selected" button with loading state

## How to Use

### For Recruiters:
1. Navigate to **Admin → Coding Problems**
2. Click **"Import from Bank"** button
3. Wait for problems to load (131 problems found)
4. Browse by category tabs:
   - Arrays
   - Dynamic Programming
   - Hashing DS
   - Linked Lists
   - Math
   - Other
   - Strings
   - Trees
5. Use "Select All" / "Deselect All" for bulk selection
6. Or check individual problems to import
7. Click **"Import Selected"** button
8. Problems are added to database (duplicates skipped)
9. Success/warning messages show import results

### Sample Problem Format:
```python
'''
Problem Title
Description and constraints
Input: [example]
Output: result
=========================================
Approach explanation
Time Complexity: O(N)
'''
def solution_function(params):
    # implementation
    pass

# Test 1
# Correct result => expected_output
print(solution_function(test_input))
```

## Parsing Logic

### What Gets Extracted:
- **Title**: First line of docstring
- **Description**: Text before "=========" separator
- **Category**: Folder name (Arrays, Dynamic Programming, etc.)
- **Difficulty**: Auto-detected based on keywords or folder
- **Function Name**: From `def function_name(...):` pattern
- **Parameters**: Function parameter list
- **Test Cases**: Parsed from Testing section comments
- **Starter Code**: Generated template from function signature

### Test Case Extraction:
- Finds `print(function_name(input))` statements
- Matches with `# Correct result => expected` comments
- First 2 test cases are visible
- Rest are hidden

## API Endpoints

### Scan Sample Problems
```http
GET /api/code/admin/import/scan
Authorization: Bearer {recruiter_token}

Response:
{
  "success": true,
  "problems": [...],
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
  "file_paths": ["path/to/problem1.py", "path/to/problem2.py"]
}

Response:
{
  "success": true,
  "imported": 5,
  "failed": 1,
  "errors": ["Problem 'Two Sum' already exists"],
  "message": "Imported 5 out of 6 problems"
}
```

## Testing

### Test Parser:
```bash
cd backend/app/CodeExecution
python problem_parser.py
```

**Output:**
```
Scanning directory: D:\...\CODING SAMPLE QUESTIONS\coding-problems
✅ Scanned 131 problems
📝 Sample problem #1:
Title: Container With Most Water
Category: Arrays
Difficulty: medium
Function: max_area(height)
Test Cases: 1
Starter Code:
def max_area(height):
    # Write your code here
    pass
```

## Notes

- **Duplicate Prevention**: System checks if problem title already exists before importing
- **Category Display**: Each tab shows number of problems in that category
- **Error Handling**: Failed imports show specific error messages
- **Selection State**: Checkbox state persists while browsing categories
- **Loading States**: UI shows spinners during scan and import operations
- **Toast Notifications**: Success/error messages appear for user feedback

## Statistics

- **Total Sample Problems**: 131
- **Categories**: 8 (Arrays, Dynamic Programming, Hashing DS, Linked Lists, Math, Other, Strings, Trees)
- **Largest Category**: Arrays (33 problems)
- **Parser Success Rate**: ~99% (1 file failed parsing due to missing function)

## Future Enhancements

1. Edit imported problems
2. Delete problems
3. View full problem details before import
4. Filter by difficulty in import dialog
5. Search problems by title/description
6. Export problems to share with other systems
