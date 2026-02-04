# Text-Based Assessment Implementation Guide

## Overview
This document describes the implementation of the text-based response feature for the HR evaluation system. This feature allows recruiters to upload open-ended questions and candidates to provide written answers (max 200 words per answer).

## Features Implemented

### Backend

#### 1. Database Models (app/models.py)
- **TextBasedQuestion**: Stores open-ended questions
  - `id`: Primary key
  - `question_id`: Unique question identifier
  - `question`: Question text
  - `created_at`: Creation timestamp
  - `updated_at`: Last update timestamp

- **TextBasedAnswer**: Stores candidate answers
  - `id`: Primary key
  - `student_id`: Foreign key to candidate_auth
  - `question_id`: Foreign key to text_based_questions
  - `answer`: The candidate's answer text
  - `word_count`: Word count of the answer
  - `submitted_at`: Submission timestamp
  - `updated_at`: Last update timestamp
  - Unique constraint: one answer per student per question

- **CandidateAuth**: Added new fields
  - `text_based_completed`: Boolean flag
  - `text_based_completed_at`: Completion timestamp

#### 2. API Routes (app/TextBased/route.py)
All routes are prefixed with `/api/text-based`

**Candidate Routes:**
- `GET /questions` - Fetch all text-based questions for candidate
- `POST /submit` - Submit or update an answer (validates 200-word limit)
- `GET /answers` - Get all answers submitted by the authenticated candidate
- `POST /complete` - Mark text-based assessment as completed

**Recruiter Routes:**
- `POST /upload` - Bulk upload questions from CSV/Excel file
- `GET /all-answers` - Get all answers from all candidates (for review)

#### 3. File Upload Format
CSV/Excel file with columns:
- `question_id` (required): Unique numeric identifier
- `question` (required): The question text

Sample file created at: `sample_text_based_upload.csv`

### Frontend

#### 1. Components Created

**TextBasedTest.tsx** (`src/pages/TextBasedTest.tsx`)
- Main candidate interface for answering text-based questions
- Features:
  - Question navigator showing all questions
  - Textarea with word count validation (max 200 words)
  - Auto-save on navigation between questions
  - Manual save button
  - Progress tracking (answered/total questions)
  - Complete test button (enabled when all questions answered)
  - Real-time word count display with warning when exceeding limit

**TextBasedUploadDialog.tsx** (`src/components/molecules/TextBasedUploadDialog.tsx`)
- Recruiter interface for uploading questions
- Features:
  - File upload (CSV/Excel)
  - Download sample template button
  - Upload progress and result display
  - Error handling with detailed error messages
  - Shows created/updated/skipped counts

#### 2. Pages Updated

**Settings.tsx** (`src/pages/admin/Settings.tsx`)
- Added "Text-Based Question Bank" section
- Includes upload button to open TextBasedUploadDialog

**CandidateHome.tsx** (`src/pages/CandidateHome.tsx`)
- Added text_based_completed tracking
- Updated assessment workflow to show 4 rounds
- Added FileText icon for text-based round
- Updated completion checks to include text-based round

**App.tsx** (`src/App.tsx`)
- Added route: `/candidate/text-based-test`
- Imported and registered TextBasedTest component

#### 3. Types Updated

**rounds.ts** (`src/types/rounds.ts`)
- Added 'text-based' to AssessmentRound type
- Added text-based configuration to ROUND_CONFIGS
- Updated ROUND_ORDER to include 'text-based' as the 4th round

## Usage Flow

### Recruiter Workflow
1. Navigate to Admin > Settings
2. Scroll to "Text-Based Question Bank" section
3. Click "Upload Questions" button
4. Download sample template (optional)
5. Select CSV/Excel file with questions
6. Click "Upload Questions"
7. Review upload results (created/updated/skipped counts)

### Candidate Workflow
1. Login and navigate to Candidate Home
2. Complete MCQ, Psychometric, and Technical rounds first
3. Click on "Text-Based Questions" from assessment workflow
4. OR navigate directly to `/candidate/text-based-test`
5. Answer each question (max 200 words)
6. Use "Save Answer" button or auto-save on navigation
7. Use question navigator to jump between questions
8. Click "Complete Test" when all questions are answered
9. Get redirected back to Candidate Home

## API Endpoints Summary

### Candidate Endpoints
```
GET  /api/text-based/questions     - Get all questions
POST /api/text-based/submit        - Submit/update answer
GET  /api/text-based/answers       - Get candidate's answers
POST /api/text-based/complete      - Mark assessment complete
```

### Recruiter Endpoints
```
POST /api/text-based/upload        - Upload questions (CSV/Excel)
GET  /api/text-based/all-answers   - Get all candidates' answers
```

## Validation Rules

### Question Upload
- Required columns: question_id, question
- question_id must be a unique integer
- question text cannot be empty
- Duplicate question_ids will update existing questions

### Answer Submission
- answer text cannot be empty
- Word count must not exceed 200 words
- Word count is calculated by splitting on whitespace
- One answer per candidate per question (unique constraint)

## Database Migrations
The app automatically creates the following tables on startup:
- `text_based_questions`
- `text_based_answers`

And adds these columns to `candidate_auth`:
- `text_based_completed` (BOOLEAN, default FALSE)
- `text_based_completed_at` (TIMESTAMP, nullable)

## Testing

### Test Data
A sample CSV file has been created at the root:
- `sample_text_based_upload.csv` (5 sample questions)

### Manual Testing Steps
1. **Backend Testing:**
   ```bash
   cd backend
   python run.py
   ```
   - Verify tables are created
   - Test upload endpoint with sample CSV
   - Test question retrieval
   - Test answer submission

2. **Frontend Testing:**
   ```bash
   cd frontend
   npm run dev
   ```
   - Test recruiter upload flow
   - Test candidate answer submission
   - Test word count validation
   - Test question navigation
   - Test auto-save functionality

## Next Steps / Potential Enhancements

1. **Recruiter Review Interface**
   - Create a page to view all candidate answers
   - Add filtering by candidate
   - Add search functionality
   - Add export to Excel feature

2. **AI Evaluation**
   - Integrate AI service to evaluate answer quality
   - Provide sentiment analysis
   - Check for plagiarism
   - Generate evaluation scores

3. **Rich Text Editor**
   - Replace textarea with rich text editor
   - Allow basic formatting (bold, italic, lists)
   - Maintain 200-word limit

4. **Analytics**
   - Average time per question
   - Most common word count
   - Question difficulty analysis

5. **Notifications**
   - Email recruiter when candidate completes text-based round
   - Notify candidate of evaluation results

## Files Modified/Created

### Backend Files
- ✅ Created: `backend/app/TextBased/__init__.py`
- ✅ Created: `backend/app/TextBased/route.py`
- ✅ Modified: `backend/app/models.py` (added 2 models, updated CandidateAuth)
- ✅ Modified: `backend/app/__init__.py` (registered blueprint, added migrations)
- ✅ Created: `sample_text_based_upload.csv`

### Frontend Files
- ✅ Created: `frontend/src/pages/TextBasedTest.tsx`
- ✅ Created: `frontend/src/components/molecules/TextBasedUploadDialog.tsx`
- ✅ Modified: `frontend/src/pages/admin/Settings.tsx`
- ✅ Modified: `frontend/src/pages/CandidateHome.tsx`
- ✅ Modified: `frontend/src/App.tsx`
- ✅ Modified: `frontend/src/types/rounds.ts`

## Notes

- The text-based assessment is the 4th and final round in the assessment workflow
- Candidates must complete MCQ, Psychometric, and Technical rounds before text-based
- Word count validation happens on both frontend and backend
- Answers are automatically saved when navigating between questions
- The assessment can be paused and resumed (answers are saved)
- All authentication uses JWT tokens (candidate/recruiter tokens)
