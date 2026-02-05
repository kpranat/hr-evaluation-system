"""
Script to clear all text-based answers from the database
Use this to remove test/sample data
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('app/.env')

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

def clear_text_based_answers():
    """Delete all text-based answers from the database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Delete all answers
        cursor.execute("DELETE FROM text_based_answers;")
        deleted_count = cursor.rowcount
        
        conn.commit()
        print(f"✅ Successfully deleted {deleted_count} text-based answers")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error clearing answers: {e}")

if __name__ == "__main__":
    confirm = input("⚠️  This will delete ALL text-based answers. Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_text_based_answers()
    else:
        print("❌ Operation cancelled")
