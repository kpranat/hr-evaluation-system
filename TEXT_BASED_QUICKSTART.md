# Text-Based Assessment - Quick Start Guide

## For Recruiters

### Upload Text-Based Questions

1. **Login as Recruiter**
   - Navigate to: `http://localhost:5173/recruiter/login`
   - Enter your credentials

2. **Access Settings**
   - Click on "Settings" in the left sidebar
   - Scroll to "Text-Based Question Bank" section

3. **Prepare Your Questions File**
   
   **Option A: Download Sample Template**
   - Click "Upload Questions" button
   - Click "Download Sample Template"
   - Edit the CSV file with your questions
   
   **Option B: Create Your Own**
   - Create a CSV or Excel file
   - Include two columns: `question_id` and `question`
   - Example:
     ```csv
     question_id,question
     1,"Describe your experience with team collaboration."
     2,"Explain a challenging problem you solved."
     ```

4. **Upload the File**
   - Click "Upload Questions" button
   - Select your CSV/Excel file
   - Click "Upload Questions"
   - Review the upload results

### View Candidate Answers

You can retrieve all candidate answers via the API:
```bash
curl -X GET http://localhost:5000/api/text-based/all-answers \
  -H "Authorization: Bearer YOUR_RECRUITER_TOKEN"
```

## For Candidates

### Complete Text-Based Assessment

1. **Login as Candidate**
   - Navigate to: `http://localhost:5173/candidate/login`
   - Enter your credentials

2. **Navigate to Assessment**
   - Complete the previous rounds (MCQ, Psychometric, Technical) first
   - Click "Continue Assessment" from the home page
   - OR directly navigate to: `http://localhost:5173/candidate/text-based-test`

3. **Answer Questions**
   - Read each question carefully
   - Type your answer in the text box
   - **Important:** Maximum 200 words per answer
   - Word count is displayed below the text box
   - Click "Save Answer" to save your progress

4. **Navigate Between Questions**
   - Use "Previous" and "Next" buttons
   - OR click on question numbers at the bottom
   - Answers auto-save when navigating

5. **Complete the Test**
   - Answer all questions
   - Click "Complete Test" button
   - You'll be redirected to the home page

### Tips for Candidates

- ✅ **Write clearly and concisely** - You have up to 200 words
- ✅ **Save frequently** - Use the "Save Answer" button or navigate between questions
- ✅ **Watch the word count** - Displayed in real-time below the text box
- ✅ **Answer all questions** - You cannot complete the test until all questions are answered
- ✅ **You can pause** - Your answers are saved, you can come back later

### Word Count Warning

If you exceed 200 words:
- The word count turns **red**
- The "Save Answer" button is disabled
- You must reduce your answer before saving

## API Endpoints Reference

### For Integration/Testing

#### Candidate Endpoints

**Get Questions**
```bash
curl -X GET http://localhost:5000/api/text-based/questions \
  -H "Authorization: Bearer CANDIDATE_TOKEN"
```

**Submit Answer**
```bash
curl -X POST http://localhost:5000/api/text-based/submit \
  -H "Authorization: Bearer CANDIDATE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "answer": "This is my answer..."
  }'
```

**Get My Answers**
```bash
curl -X GET http://localhost:5000/api/text-based/answers \
  -H "Authorization: Bearer CANDIDATE_TOKEN"
```

**Complete Test**
```bash
curl -X POST http://localhost:5000/api/text-based/complete \
  -H "Authorization: Bearer CANDIDATE_TOKEN"
```

#### Recruiter Endpoints

**Upload Questions**
```bash
curl -X POST http://localhost:5000/api/text-based/upload \
  -H "Authorization: Bearer RECRUITER_TOKEN" \
  -F "file=@sample_text_based_upload.csv"
```

**Get All Answers**
```bash
curl -X GET http://localhost:5000/api/text-based/all-answers \
  -H "Authorization: Bearer RECRUITER_TOKEN"
```

## Troubleshooting

### Backend Issues

**Problem:** Tables not created
```bash
# Solution: Restart the backend server
cd backend
python run.py
```

**Problem:** Upload fails
- Check file format (CSV or Excel)
- Verify columns: question_id, question
- Ensure question_id is a number

### Frontend Issues

**Problem:** Cannot save answer
- Check word count (must be ≤ 200 words)
- Check network connection
- Verify authentication token

**Problem:** Cannot complete test
- Ensure all questions are answered
- Check for any unsaved changes

## Sample Questions File

Located at: `sample_text_based_upload.csv`

Contains 5 sample questions:
1. Team collaboration and conflict handling
2. Technical problem solving
3. Professional motivation
4. Learning new technologies
5. Task prioritization

## Next Steps

After implementing the basic feature, consider:
1. Creating a recruiter dashboard to review answers
2. Adding AI-powered evaluation
3. Implementing answer export functionality
4. Adding candidate answer history/revision tracking
