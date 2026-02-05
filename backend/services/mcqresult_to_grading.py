import json
import os

def evaluate_mcq_performance(correct_answers, total_questions):
    """
    Input:
        - correct_answers (int)
        - total_questions (int)
        
    Output: JSON object { "percentage": float }
    """
    if total_questions == 0:
        percentage = 0.0
    else:
        percentage = (correct_answers / total_questions) * 100
        
    return {
        "percentage": round(percentage, 2)
    }

def save_to_example_file(data):
    """
    Takes the JSON output and saves it to example.txt in the same directory,
    overwriting any existing content.
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.txt')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Result saved to {file_path}")

if __name__ == "__main__":
    # Test Data
    total = 20
    correct = 18
    
    print(f"Calculating MCQ percentage for {correct}/{total}...")
    result = evaluate_mcq_performance(correct, total)
    print("Result:", json.dumps(result, indent=2))
    save_to_example_file(result)

