import os
from groq import Groq
import json

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Helper to clean AI output (removes markdown formatting)
def clean_json_output(response_text):
    return response_text.replace("```json", "").replace("```", "").strip()

#============================================================#
# Resume Parser
#============================================================#
def parse_resume_to_json(resume_text):
    """
    Input: Raw string text extracted from PDF.
    Output: JSON object { "name": str, "email": str, "skills": list, "experience_years": int }
    """
    prompt = f"""
    Extract the following details from the resume text below:
    - Name
    - Email
    - List of Technical Skills
    - Total Years of Experience (Integer)

    Resume Text:
    {resume_text}

    Return ONLY valid JSON. No preamble.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    return json.loads(clean_json_output(response.choices[0].message.content))

#============================================================#
# Response Grader
#============================================================#
def grade_text_response(question, user_answer):
    """
    Input: The question text and the candidate's answer string.
    Output: JSON object { "score": int (0-100), "feedback": str }
    """
    prompt = f"""
    Evaluate this answer for clarity, logic, and depth.
    Question: {question}
    Answer: {user_answer}
    
    Give a score from 0-100 and a 1-sentence feedback.
    Return ONLY JSON: {{ "score": <int>, "feedback": "<string>" }}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    return json.loads(clean_json_output(response.choices[0].message.content))

#============================================================#
# Integrity Log Analyzer
#============================================================#
def analyze_integrity_logs(log_array):
    """
    Input: List of logs e.g. [{"time": "10:00", "event": "tab_switch"}]
    Output: String ("Low Risk", "Medium Risk", "High Risk")
    """
    if not log_array:
        return "Low Risk"

    prompt = f"""
    Analyze these proctoring logs for a coding test:
    {json.dumps(log_array)}
    
    Rules:
    - Frequent tab switching = High Risk
    - Multiple faces detected = High Risk
    - No face detected for long periods = Medium Risk
    
    Return ONLY one string: "Low Risk", "Medium Risk", or "High Risk".
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    return response.choices[0].message.content.strip()

#============================================================#
# Generate Verdict
#============================================================#
def generate_final_verdict(candidate_data, technical_score, soft_skill_score, integrity_risk):
    """
    Input: Aggregated data from all previous steps.
    Output: JSON { "decision": "Hire"|"No Hire", "rationale": str, "strengths": list, "weaknesses": list }
    """
    prompt = f"""
    Act as a Senior Technical Recruiter. Make a hiring decision based on this data:
    
    Candidate: {candidate_data.get('name')}
    Technical Score: {technical_score}/100
    Soft Skill Score: {soft_skill_score}/100
    Integrity Risk: {integrity_risk}
    
    1. Decision: Hire or No Hire.
    2. Rationale: 3 sentences justifying the decision.
    3. Strengths: 3 keywords.
    4. Weaknesses: 3 keywords.
    
    Return ONLY valid JSON.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", # Using the larger model for reasoning
    )
    
    return json.loads(clean_json_output(response.choices[0].message.content))