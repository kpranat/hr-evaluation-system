# Technical Documentation

## 1. System Architecture

The HR Evaluation Platform follows a **Client-Server architecture**:
*   **Frontend**: A Single Page Application (SPA) built with React and Vite. It communicates with the backend via RESTful APIs using JWT for authentication.
*   **Backend**: A monolithic Flask application organized using **Blueprints** to separate concerns (Auth, Proctoring, Assessment).
*   **Database**: PostgreSQL serves as the primary data store for user data, assessment configs, and results.

## 2. Backend Modules (Flask Blueprints)

The backend is divided into several logical modules:

### 2.1 Core Services
*   **`app/services/ai_service.py`**: Handles computer vision tasks.
    *   **Input**: Base64 encoded image frames.
    *   **Processing**: Uses `cv2` (OpenCV) for image decoding and `mediapipe` for Face Detection, Face Mesh (Gaze), and Hand Detection.
    *   **Output**: Violation report (No Face, Multiple Faces, Looking Away, Phone Detected).
*   **`app/services/coding_question_bank.py`**: Manages the file-based coding question repository.

### 2.2 Blueprints
*   **`CandidateAuth` / `RecruiterAuth`**: Handles login, registration (recruiter), and token issuance.
*   **`ProctorService`**:
    *   `POST /session/start`: Initializes a proctoring session.
    *   `POST /analyze-frame`: Receives video snapshots from the client, calls `ai_service`, logs violations to DB.
    *   `GET /session/{id}/summary`: Returns aggregated violation data.
*   **`CodeExecution`**: Manages coding tests, problem fetching, and submission grading.
*   **`MCQ` / `TextBased` / `Psychometric`**: Manage specific assessment types.

## 3. Database Schema (PostgreSQL)

Key entities in the system:

*   **`CandidateAuth`**: Stores candidate credentials and global progress flags (`mcq_completed`, `technical_completed`, etc.).
*   **`ProctorSession`**: Represents a single proctoring run. Links to `Candidate` and `Assessment`.
*   **`ProctoringViolation`**: specific violation events linked to a session.
    *   Fields: `violation_type` (enum), `severity`, `violation_data` (JSON details), `timestamp`.
*   **`CodingProblem`**: Stores imported problems (Title, Description, Test Cases).
*   **`CodingSubmission`**: Stores candidate code and execution results.

## 4. Proctoring Workflow

1.  **Initialization**: Frontend requests camera permissions and calls `/session/start`.
2.  **Monitoring Loop**:
    *   Frontend `useFaceDetection` hook captures a video frame every ~2 seconds.
    *   Frame is drawn to a hidden canvas and converted to Base64 (JPEG).
    *   Frame is POSTed to `/api/proctor/analyze-frame`.
3.  **Analysis**:
    *   Backend `ai_service` analyzes the frame.
    *   If a violation is detected (e.g., face looking away > 15 degrees), it is logged to the DB.
    *   Response includes the analysis result.
4.  **Feedback**: Frontend receives the response and triggers local callbacks (e.g., showing a warning toast).

## 5. Coding Import System

The platform supports a "Hybrid" question bank:
*   **Source**: Local directory `CODING SAMPLE QUESTIONS/`.
*   **Process**:
    *   Recruiter scans the directory via Admin Dashboard.
    *   Selected files are parsed (extracting Title, Description, Test Cases).
    *   Structured data is inserted into the PostgreSQL `coding_problems` table.
*   **Benefit**: Allows easy version control of questions (git) while providing database-speed access during tests.

## 6. Frontend Architecture

*   **Routing**: `react-router-dom` manages navigation between Assessment types.
*   **State**: `localStorage` is used for persisting Auth Tokens (`candidate_token`, `recruiterToken`).
*   **Components**:
    *   `useFaceDetection`: Custom hook that encapsulates the proctoring logic.
    *   `CodeEditor`: Monaco Editor integration for coding tests.
