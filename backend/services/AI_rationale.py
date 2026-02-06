import json
import os
import sys

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import CandidateAuth, MCQResult, PsychometricResult, TextAssessmentResult, CandidateRationale, CodingAssessmentResult, ProctorSession
from services.placeholder_functions import client, clean_json_output
from services.coding_result_to_grading import process_coding_grading
from services.proctor_result_to_grading import process_proctor_grading

def generate_final_rationale(resume_data, mcq_score, text_remark, psychometric_analysis, coding_data, proctor_data):
    """
    Inputs: Data objects/dicts from previous steps.
    Output: JSON object with final verdict.
    """
    prompt = f"""
    Act as a Senior Technical Recruiter and Assessment Expert.
    Your goal is to provide a comprehensive, transparent, and balanced evaluation of the candidate.
    
    DATA PROVIDED:
    
    1. RESUME DATA:
    {json.dumps(resume_data, indent=2) if isinstance(resume_data, dict) else resume_data}
    
    2. TECHNICAL SCORE (MCQ Based):
    {json.dumps(mcq_score, indent=2) if isinstance(mcq_score, dict) else mcq_score}
    
    3. SOFT SKILLS (Text Assessment Based):
    {json.dumps(text_remark, indent=2) if isinstance(text_remark, dict) else text_remark}
    
    4. PSYCHOMETRIC TRAITS (For Reference Only - Do NOT grade pass/fail):
    {json.dumps(psychometric_analysis, indent=2) if isinstance(psychometric_analysis, dict) else psychometric_analysis}

    5. CODING SKILLS (Sandbox Result):
    {json.dumps(coding_data, indent=2) if isinstance(coding_data, dict) else coding_data}

    6. PROCTORING / INTEGRITY (Malpractice Check):
    {json.dumps(proctor_data, indent=2) if isinstance(proctor_data, dict) else proctor_data}
    
    INSTRUCTIONS:
    Analyze the candidate data to produce a Final Rationale Report.
    
    SCORING RULES:
    - Write each section as a DETAILED PARAGRAPH (3-5 sentences each).
    - PRIORITIZE: Resume Fit -> describe why the resume fits or doesn't fit in detail.
    - Coding Skills: Detailed analysis of coding performance, problems solved, code quality.
    - Soft Skills: Detailed analysis of communication, clarity, professionalism from Text Assessment.
    - Psychometric: Brief personality insight (2-3 sentences). Low priority for hiring decision.
    
    INTEGRITY RULES (IMPORTANT):
    - If Integrity/Fairplay score is ABOVE 50: Do NOT penalize the candidate. Consider it acceptable.
    - If Integrity/Fairplay score is BELOW 50: Mention this as an observation ONLY. Do NOT let it affect the hiring decision. Simply inform the recruiter that there were some concerns.
    - NEVER reject a candidate solely based on integrity score. It is informational only.
    
    FORMAT REQUIREMENTS:
    - Each section should be a FULL PARAGRAPH, not a single sentence.
    - Use professional language and provide specific insights.
    - Cite actual scores and data in your reasoning.
    
    CRITICALITY GUIDELINES:
    - Be fair: If a candidate has a good Technical Score (e.g. >70%), they should generally NOT be rated "Poor" overall unless Soft Skills are terrible.
    - Contextualize: High Technical + Low Soft Skills = Potential Individual Contributor. Low Technical + High Soft Skills = Potential Jr/Support role.
    
    TRANSPARENCY REQUIREMENT:
    - In the "reasoning" for each section, explicitely cite the scores (e.g., "...given the Technical Score of 85%..." or "...Communication Score of 75/100...").
    
    OUTPUT FORMAT:
    Return ONLY valid JSON in the following format:
    {{
        "resume_fit": {{
            "grade": "Excellent" | "Good" | "Average" | "Poor",
            "reasoning": "3-5 sentences. Detailed analysis of how well the resume matches the role requirements."
        }},
        "technical_evaluation": {{
            "grade": "Excellent" | "Good" | "Average" | "Poor",
            "reasoning": "3-5 sentences. Detailed analysis of MCQ performance, knowledge areas, strengths and gaps."
        }},
        "coding_evaluation": {{
            "grade": "Excellent" | "Good" | "Average" | "Poor",
            "reasoning": "3-5 sentences. Detailed analysis of coding problems solved, approach, and code quality."
        }},
        "soft_skills_evaluation": {{
            "grade": "Excellent" | "Good" | "Average" | "Poor",
            "reasoning": "3-5 sentences. Detailed analysis of communication skills, clarity, and professionalism."
        }},
        "psychometric_evaluation": {{
            "grade": "Insight" | "Neutral",
            "reasoning": "2-3 sentences. Brief personality insight - NOT a pass/fail judgment."
        }},
        "integrity_observation": {{
            "status": "Acceptable" | "Observation",
            "reasoning": "2-3 sentences. If score > 50, mark as Acceptable. If score < 50, note the observation but do NOT penalize."
        }},
        "final_decision": {{
             "status": "Hire" | "No Hire" | "Strong Hire" | "Consider for Future",
             "summary": "4-6 sentences. Comprehensive final verdict synthesizing all evaluations. Do NOT penalize for integrity unless it's directly relevant to role requirements."
        }}
    }}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return json.loads(clean_json_output(response.choices[0].message.content))
    except Exception as e:
        print(f"Error generating rationale: {e}")
        return {"error": str(e)}

def generate_psychometric_narrative(traits_data):
    """
    Uses a smaller, faster model (Llama-3 8b) to convert raw trait scores into a readable paragraph.
    Input: Dict of traits {'extraversion': 3.5, ...}
    Output: String (paragraph)
    """
    prompt = f"""
    Act as an Industrial-Organizational Psychologist.
    Convert the following Big Five personality trait scores (0-5 scale) into a single, professional, easy-to-read paragraph summarizing the candidate's personality profile.
    
    TRAIT SCORES:
    {json.dumps(traits_data, indent=2)}
    
    GUIDELINES:
    - Do NOT list the scores numbers in the text.
    - Focus on behaviors: e.g., "The candidate is highly organized..." instead of "Conscientiousness is 4.5".
    - Be balanced and professional.
    - Keep it under 80 words.
    - Return ONLY the paragraph text. No JSON, no intro.
    """
    
    try:
        # User requested 70b for better quality even for summary if possible, but 8b is fast.
        # User said "use 70b model for generating output instead of 8b" generally.
        # Let's switch this to 70b as well to be safe and high quality.
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", 
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating psychometric narrative: {e}")
        return "Psychometric analysis available but narrative generation failed."

def process_ai_rationale(candidate_id, app_instance=None):
    """
    Fetches all candidate data, generates rationale, and saves to DB.
    """
    # Use provided app instance or create new one
    app = app_instance if app_instance else create_app()
    context = app.app_context() if not app_instance else None
    
    # Enter context if we created it
    if context:
        context.push()

    try:
        print(f"🔄 Fetching raw score data for Candidate {candidate_id}...")
        
        # 1. Resume Data
        candidate = CandidateAuth.query.get(candidate_id)
        if not candidate:
             print(f"❌ Candidate {candidate_id} not found.")
             return None
        resume_data = candidate.resume_data if candidate.resume_data else {"error": "Resume data not processed yet."}
        
        # 2. MCQ Data (Raw Score)
        mcq_result = MCQResult.query.filter_by(student_id=candidate_id).first()
        if mcq_result:
            mcq_data = {
                "percentage": mcq_result.percentage_correct,
                "correct": mcq_result.correct_answers,
                "total": mcq_result.correct_answers + mcq_result.wrong_answers
            }
        else:
            mcq_data = {"percentage": 0, "error": "MCQ not taken."}
        
        # 3. Psychometric Data (Raw Traits)
        psycho_result = PsychometricResult.query.filter_by(student_id=candidate_id).first()
        if psycho_result:
            # Map 0-50 scores to 0-5 for clarity in prompt
            psycho_data = {
                "extraversion": round(psycho_result.extraversion / 10, 1),
                "agreeableness": round(psycho_result.agreeableness / 10, 1),
                "conscientiousness": round(psycho_result.conscientiousness / 10, 1),
                "emotional_stability": round(psycho_result.emotional_stability / 10, 1),
                "intellect_imagination": round(psycho_result.intellect_imagination / 10, 1)
            }
        else:
            psycho_data = {"error": "Psychometric not taken."}
        
        # 4. Text Assessment Data (Grading JSON directly)
        text_result = TextAssessmentResult.query.filter_by(candidate_id=candidate_id).first()
        text_data = text_result.grading_json if text_result and text_result.grading_json else {"error": "Text responses not graded yet."}

        # 5. Coding Data
        coding_result = CodingAssessmentResult.query.filter_by(candidate_id=candidate_id).first()
        if coding_result and coding_result.grading_json:
             coding_data = coding_result.grading_json
        else:
             # Try grading on the fly if missing
             coding_data = process_coding_grading(candidate_id, app) or {"error": "Coding not submitted."}

        # 6. Proctor Data
        # Fetch latest session to check grading
        last_session = ProctorSession.query.filter_by(candidate_id=candidate_id).order_by(ProctorSession.start_time.desc()).first()
        if last_session and last_session.grading_json:
            proctor_data = last_session.grading_json
        else:
            proctor_data = process_proctor_grading(candidate_id, app) or {"severity": "Unknown", "remark": "No session data."}

        
        print("🤖 Generating Final Rationale (Llama-70b)...")
        rationale_data = generate_final_rationale(resume_data, mcq_data, text_data, psycho_data, coding_data, proctor_data)
        
        # 5. Generate Readable Psychometric Summary (Llama-8b)
        if psycho_result:
            print("🧠 Generating Psychometric Narrative (Llama-8b)...")
            psycho_narrative = generate_psychometric_narrative(psycho_data)
            
            # Inject into the main rationale JSON
            if "psychometric_evaluation" in rationale_data:
                rationale_data["psychometric_evaluation"]["reasoning"] = psycho_narrative
                # Or keep the old reasoning and add this as summary? 
                # User request: "converts it into a neat formal paragraph which is easily readable"
                # Replacing 'reasoning' seems best as that's what is displayed on the frontend.
            else:
                 rationale_data["psychometric_evaluation"] = {
                     "grade": "Insight",
                     "reasoning": psycho_narrative
                 }
        
        # Save to DB
        rationale_record = CandidateRationale.query.filter_by(candidate_id=candidate_id).first()
        if not rationale_record:
            rationale_record = CandidateRationale(candidate_id=candidate_id)
            db.session.add(rationale_record)
            
        rationale_record.rationale_json = rationale_data
        db.session.commit()
        print(f"✅ Final Rationale saved for Candidate {candidate_id}")
        return rationale_data
        
    except Exception as e:
        print(f"Error in process_ai_rationale: {e}")
        return None
    finally:
        if context:
            context.pop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 AI_rationale.py <candidate_id>")
        sys.exit(1)
        
    candidate_id = int(sys.argv[1])
    
    result = process_ai_rationale(candidate_id)
    
    if result:
        # Save to AI_rationale.txt as requested in original requirements/logic
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI_rationale.txt')
        with open(file_path, 'w') as f:
            f.write(json.dumps(result, indent=4))
        print(f"✅ Output also saved to {file_path}")
