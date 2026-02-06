# Proctoring System Test Guide

This guide explains how to test the new OpenCV-based backend proctoring system.

## Prerequisites
1.  **Backend**: Ensure the backend is running and `mediapipe` is installed.
    ```bash
    cd backend
    pip install -r requirements.txt
    python run.py
    ```
2.  **Frontend**: Ensure the frontend is running.
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## Testing Steps

### 1. Start an Assessment
*   Log in as a candidate.
*   Start any assessment (e.g., Coding, MCQ) that has proctoring enabled.
*   Ensure you grant camera permissions when prompted.

### 2. Verify Face Detection
*   **Normal**: Sit in front of the camera. The system should not trigger any warnings.
*   **No Face**: Cover your camera or move out of frame.
    *   *Expected Result*: A "No face detected" violation should be logged/displayed.
*   **Multiple Faces**: Have another person stand next to you.
    *   *Expected Result*: A "Multiple faces detected" violation should be logged.

### 3. Verify Advanced Features (New)
*   **Looking Away**: Turn your head significantly to the left, right, or down for a few seconds.
    *   *Expected Result*: A "Looking away" violation should be logged.
*   **Suspicious Object/Hand**: Raise your hand near your face (e.g., as if holding a phone to your ear or covering your mouth).
    *   *Expected Result*: A "Suspicious object/hand detected" violation should be logged.

### 4. Verify Logs
*   Check the backend console output. You should see colorful logs like:
    ```
    [PROCTOR WARNING] 10:30:45
      Event: LOOKING_AWAY
      Details: Looking Right
    ```
*   These events are also stored in the database under `proctoring_violations`.

## Troubleshooting
*   If the camera doesn't start, check browser permissions.
*   If violations are not triggered, ensure the backend is reachable at `/api/proctor/analyze-frame`.
*   Check the browser console for network errors if frontend verification fails.
