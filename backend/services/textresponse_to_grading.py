import json
import os
from placeholder_functions import client, clean_json_output

def evaluate_text_responses(qa_pairs):
    """
    Input: qa_pairs (List[Dict]) - List of { "question": str, "answer": str }
    Output: JSON String { "remark": "One sentence summary..." }
    """
    prompt = f"""
    Analyze the following Candidate Q&A responses:
    {json.dumps(qa_pairs, indent=2)}
    
    Task:
    Read all the answers and provide a SINGLE, comprehensive sentence remarking on the candidate's communication skills, depth of understanding, and clarity. Be very critical and keep the tone professional.
    
    Return ONLY valid JSON: {{ "remark": "<one sentence string>" }}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    # We clean the output first, then load it to ensure valid JSON, then dump it back to string
    # This ensures we return a valid JSON string as requested
    cleaned_text = clean_json_output(response.choices[0].message.content)
    try:
        data = json.loads(cleaned_text)
        return json.dumps(data)
    except:
        # Fallback if AI returns malformed JSON
        return json.dumps({"remark": "Unable to analyze responses."})

def save_to_example_file(json_string):
    """
    Takes the JSON string and saves it to example.txt.
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.txt')
    with open(file_path, 'w') as f:
        f.write(json_string)

if __name__ == "__main__":
    # Test Data
    sample_qa = [
        {
            "question": "Explain the concept of Dependency Injection.",
            "answer": "Dependency injection is a design pattern where an object receives other objects that it depends on. It promotes loose coupling and makes code easier to test."
        },
        {
            "question": "What is the difference between a process and a thread?",
            "answer": "A process is an instance of a program in execution, having its own memory space. A thread is a lightweight process that shares memory with other threads within the same process."
        }
    ]
    
    json_output = evaluate_text_responses(sample_qa)
    print(json_output)
    save_to_example_file(json_output)
