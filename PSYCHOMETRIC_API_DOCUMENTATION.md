# Psychometric Assessment API Documentation

## Overview
The psychometric assessment uses the IPIP Big Five Factor Markers to evaluate candidates on 5 personality traits:
1. **Extraversion** - Sociability, assertiveness, energy
2. **Agreeableness** - Trust, altruism, cooperation
3. **Conscientiousness** - Organization, responsibility, dependability
4. **Emotional Stability** - Calmness, emotional resilience (opposite of Neuroticism)
5. **Intellect/Imagination** - Curiosity, creativity, open-mindedness

## Database Tables Created

### 1. `psychometric_questions`
Stores all 50 IPIP Big Five questions
- `id` - Primary key
- `question_id` - Unique question identifier (1-50)
- `question` - Question text
- `trait_type` - Which Big Five trait (1-5)
- `scoring_direction` - '+' for normal, '-' for reverse scoring
- `is_active` - Whether question is in current pool

### 2. `psychometric_test_config`
Stores recruiter's test configuration
- `recruiter_id` - Foreign key to recruiter_auth
- `num_questions` - How many questions to show
- `selection_mode` - 'random' or 'manual'
- `selected_question_ids` - JSON array of manually selected IDs
- `is_active` - Whether this config is active

### 3. `psychometric_results`
Stores candidate personality scores
- `student_id` - Foreign key to candidate_auth
- `extraversion` - Score (0-50)
- `agreeableness` - Score (0-50)
- `conscientiousness` - Score (0-50)
- `emotional_stability` - Score (0-50)
- `intellect_imagination` - Score (0-50)
- `answers_json` - JSON of all answers

## API Endpoints

### Admin/Recruiter Routes

#### 1. Load Questions (One-time Setup)
```
POST /api/psychometric/load-questions
```
Loads all 50 IPIP Big Five questions into the database.

**Response:**
```json
{
  "success": true,
  "message": "Successfully loaded 50 psychometric questions",
  "count": 50
}
```

#### 2. Get All Questions
```
GET /api/psychometric/questions/all
```
Retrieves all psychometric questions (for recruiter dashboard).

**Response:**
```json
{
  "success": true,
  "total_questions": 50,
  "questions": [...],
  "grouped_by_trait": {
    "Extraversion": [...],
    "Agreeableness": [...],
    ...
  }
}
```

#### 3. Set Test Configuration
```
POST /api/psychometric/config/set
```

**Request Body (Random Selection):**
```json
{
  "recruiter_id": 1,
  "num_questions": 30,
  "selection_mode": "random"
}
```

**Request Body (Manual Selection):**
```json
{
  "recruiter_id": 1,
  "num_questions": 10,
  "selection_mode": "manual",
  "selected_question_ids": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Test configuration saved successfully",
  "config": {...}
}
```

#### 4. Get Current Configuration
```
GET /api/psychometric/config/current?recruiter_id=1
```

**Response:**
```json
{
  "success": true,
  "config": {
    "id": 1,
    "recruiter_id": 1,
    "num_questions": 30,
    "selection_mode": "random",
    "is_active": true
  }
}
```

### Candidate Routes

#### 5. Start Test
```
POST /api/psychometric/test/start
```

**Request Body:**
```json
{
  "candidate_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "instructions": "Describe yourself as you generally are now...",
  "total_questions": 30,
  "questions": [
    {
      "id": 1,
      "question_id": 5,
      "question": "Have a rich vocabulary.",
      "trait_type": 5,
      "scoring_direction": "+"
    },
    ...
  ],
  "answer_options": [
    {"value": 1, "label": "Very Inaccurate"},
    {"value": 2, "label": "Moderately Inaccurate"},
    {"value": 3, "label": "Neither Accurate Nor Inaccurate"},
    {"value": 4, "label": "Moderately Accurate"},
    {"value": 5, "label": "Very Accurate"}
  ]
}
```

#### 6. Submit Test
```
POST /api/psychometric/test/submit
```

**Request Body:**
```json
{
  "candidate_id": 1,
  "answers": [
    {"question_id": 5, "answer": 4},
    {"question_id": 12, "answer": 2},
    ...
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Psychometric test completed successfully",
  "results": {
    "extraversion": 35,
    "agreeableness": 42,
    "conscientiousness": 38,
    "emotional_stability": 40,
    "intellect_imagination": 45
  },
  "trait_names": {
    "1": "Extraversion",
    "2": "Agreeableness",
    "3": "Conscientiousness",
    "4": "Emotional Stability",
    "5": "Intellect/Imagination"
  }
}
```

#### 7. Get Candidate Results
```
GET /api/psychometric/results/{candidate_id}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "student_id": 1,
    "extraversion": 35,
    "agreeableness": 42,
    "conscientiousness": 38,
    "emotional_stability": 40,
    "intellect_imagination": 45,
    "questions_answered": 30,
    "test_completed": true,
    "trait_names": {...}
  }
}
```

## Scoring Logic

### Answer Scale
Candidates respond on a 5-point Likert scale:
1. Very Inaccurate
2. Moderately Inaccurate
3. Neither Accurate Nor Inaccurate
4. Moderately Accurate
5. Very Accurate

### Scoring Direction
- **Positive (+)**: Score = answer value (1-5)
- **Negative (-)**: Score = 6 - answer value (reverse scoring)

Example:
- Question: "Am the life of the party" (Extraversion, +)
  - Answer: 5 (Very Accurate) → Score: 5
- Question: "Don't talk a lot" (Extraversion, -)
  - Answer: 5 (Very Accurate) → Score: 1 (6-5)

### Final Scores
Each trait score is the sum of all related question scores. With 10 questions per trait, scores range from 10-50.

## Workflow

### Recruiter Side:
1. **Load Questions** (one-time): `POST /api/psychometric/load-questions`
2. **View Questions**: `GET /api/psychometric/questions/all`
3. **Configure Test**: `POST /api/psychometric/config/set`
   - Choose number of questions
   - Choose random or manual selection
   - If manual, select specific question IDs
4. **View Config**: `GET /api/psychometric/config/current`

### Candidate Side:
1. **Start Test**: `POST /api/psychometric/test/start`
   - Receives instructions and questions
2. **Answer Questions**: Frontend handles Q&A flow
3. **Submit Test**: `POST /api/psychometric/test/submit`
   - Scores calculated automatically
   - Results stored in database
   - `psychometric_completed` flag set to true
4. **View Results**: `GET /api/psychometric/results/{id}`

## Integration Notes

- Questions are displayed in **random order** to each candidate
- Recruiter can configure test **before** candidates start
- If no config exists, **all 50 questions** are used by default
- Candidates can only take the test **once** (results are updated if retaken)
- Completion status is tracked in `candidate_auth` table
- Frontend already has types defined for psychometric round

## Next Steps

To integrate with recruiter dashboard:
1. Add UI for viewing all questions
2. Add UI for selecting questions (checkboxes)
3. Add input for number of questions
4. Add radio buttons for random/manual mode
5. Show current active configuration
6. Display candidate results in dashboard
