# Technical Documentation - HR Evaluation System

## Architecture Overview

The HR Evaluation System is a modern, AI-powered assessment platform designed to streamline candidate evaluation. It employs a decoupled client-server architecture:

-   **Frontend**: A responsive Single Page Application (SPA) built with React and TypeScript.
-   **Backend**: A RESTful API built with Flask (Python), handling business logic, database interactions, and AI integrations.
-   **Database**: PostgreSQL for persistent storage of user data, assessments, and results.
-   **AI Services**: Groq for high-performance LLM inference (grading, rationale generation) and client-side models for proctoring.

## Technology Stack

### Frontend
-   **Framework**: React (Vite)
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS
-   **UI Components**: Shadcn UI / Radix primitives
-   **State Management**: React Hooks (Context API / Local State)
-   **AI/ML**: 
    -   `face-api.js` / `mediapipe` (implied) for facial detection.
    -   Web Audio API for sound detection.

### Backend
-   **Framework**: Flask (Python)
-   **Database ORM**: SQLAlchemy
-   **Authentication**: JWT (PyJWT) & Supabase
-   **AI Integration**: Groq API (likely Llama 3 via Groq)
-   **Utilities**: 
    -   `pandas` / `numpy` for data processing.
    -   `pypdf` for resume parsing.
    -   `openpyxl` for Excel report generation.

### Database
-   **PostgreSQL**: Primary relational database.

## Key Modules

### 1. Assessment Engine
The core module responsible for delivering various types of tests:
-   **MCQ**: Multiple Choice Questions.
-   **Psychometric**: Personality and behavioral traits assessment.
-   **Coding**: Integrated code editor for programming challenges.
-   **Text-Based**: Open-ended questions graded by AI.

### 2. AI Proctoring System
A real-time monitoring system ensuring assessment integrity:
-   **Face Detection**: Detects presence/absence of face, multiple faces, and looking away events.
-   **Audio Detection**: Monitors suspicious noise levels.
-   **Activity Monitoring**: Tracks tab switching, copy-paste events, and mouse exits.
-   **Violation Logging**: automatically flags and logs suspicious activities for recruiter review.

### 3. Automated Grading & Insights
-   **AI Grading**: Text-based answers are evaluated by LLMs via Groq for relevance, clarity, and correctness.
-   **Resume Parsing**: Extracts candidate skills and experience from PDFs.
-   **Reports**: Generates detailed JSON and Excel reports for recruiters.

## Setup & Installation

### Prerequisites
-   Node.js (v18+)
-   Python (v3.10+)
-   PostgreSQL
-   Groq API Key
-   Supabase Credentials

### Backend Setup
1.  Navigate to `backend/`.
2.  Create a virtual environment: `python -m venv venv`.
3.  Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
4.  Install dependencies: `pip install -r requirements.txt`.
5.  Configure `.env` with database URL and API keys.
6.  Run server: `python run.py`.

### Frontend Setup
1.  Navigate to `frontend/`.
2.  Install dependencies: `npm install`.
3.  Run development server: `npm run dev`.

## Directory Structure

```
root/
├── backend/            # Flask API
│   ├── app/            # Application routes and models
│   ├── services/       # Business logic (AI, grading)
│   └── requirements.txt
├── frontend/           # React App
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── hooks/      # Custom React hooks (useProctoring, etc.)
│   │   ├── pages/      # Route pages
│   │   └── lib/        # Utilities and API clients
│   └── vite.config.ts
└── TECHNICAL.md        # This file
```
