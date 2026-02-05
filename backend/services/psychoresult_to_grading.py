import json
import os
from placeholder_functions import client, clean_json_output


def evaluate_psychometric_match(psychometric_scores, target_trait):
    """
    Input: 
        psychometric_scores: Dict { "Extraversion": float, "Agreeableness": float, ... }
        target_trait: String (e.g., "Conscientiousness") or None
    Output: JSON object { "match_grade": "High"|"Medium"|"Low", "analysis": str }
    """
    if not target_trait:
        return {
            "match_grade": "N/A",
            "analysis": "No target trait specified. Psychometric profile is neutral."
        }

    prompt = f"""
    Evaluate the candidate's psychometric fit for a role requiring high {target_trait}.
    
    Candidate Scores (0-10 scale or similar):
    {json.dumps(psychometric_scores, indent=2)}
    
    Target Trait: {target_trait}
    
    1. Determine if the candidate's score for the Target Trait (and related traits) makes them a good fit.
    2. Assign a Grade: "High Match", "Medium Match", or "Low Match".
    3. Write a 1-sentence analysis.
    
    Return ONLY valid JSON: {{ "match_grade": "<string>", "analysis": "<string>" }}
    """
    
    # Using 8b model as requested for efficiency
    # Note: client and clean_json_output need to be imported or defined
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    return json.loads(clean_json_output(response.choices[0].message.content))

# def save_to_example_file(data):
#     """
#     Takes the JSON output and saves it to example.txt in the same directory,
#     overwriting any existing content.
#     """
#     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.txt')
#     with open(file_path, 'w') as f:
#         json.dump(data, f, indent=4)
#     print(f"✅ Result saved to {file_path}")
# if __name__ == "__main__":
#     test_scores = {
#         "Extraversion": 80,
#         "Agreeableness": 75,
#         "Conscientiousness": 90,
#         "Emotional Stability": 70,
#         "Intellect/Imagination": 85
#     }
#     target = "Conscientiousness"
    
#     print(f"Running evaluation for {target}...")
#     result = evaluate_psychometric_match(test_scores, target)
#     print("Match Result:", result)
#     save_to_example_file(result)
