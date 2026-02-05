
import os
from groq import Groq

def list_models():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set")
        return

    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        
        print(f"Found {len(models.data)} models:")
        for m in models.data:
            print(f"- {m.id}")
            
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_models()
