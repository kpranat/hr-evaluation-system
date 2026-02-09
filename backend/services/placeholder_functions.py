"""
Placeholder functions for AI-powered resume parsing and grading.
Uses Groq API for natural language processing tasks.  
"""
import os
import re
from groq import Groq

# Initialize Groq client
# Make sure to set GROQ_API_KEY in your .env file
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def clean_json_output(text):
    """
    Clean and extract valid JSON from LLM response.
    Removes markdown code blocks, extra whitespace, and other formatting.
    
    Args:
        text (str): Raw text response from LLM
        
    Returns:
        str: Cleaned JSON string ready for parsing
    """
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Remove any leading/trailing whitespace
    text = text.strip()
    
    # Find JSON object or array (handles both {} and [])
    json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    return text
