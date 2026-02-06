"""
Create Coding Question Bank Table in PostgreSQL

This script creates the coding_question_bank table in your local PostgreSQL database.
This is separate from Supabase - it's for local development if needed.

Usage:
    python create_question_bank_table.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import CodingQuestionBank


def create_question_bank_table():
    """Create the coding_question_bank table in PostgreSQL"""
    print("\n" + "="*70)
    print("🗄️  CREATE QUESTION BANK TABLE: PostgreSQL")
    print("="*70 + "\n")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if table already exists
            inspector = db.inspect(db.engine)
            if 'coding_question_bank' in inspector.get_table_names():
                print("ℹ️  Table 'coding_question_bank' already exists")
                print("   Skipping creation...\n")
                return
            
            # Create the table
            print("📝 Creating 'coding_question_bank' table...")
            CodingQuestionBank.__table__.create(db.engine)
            
            print("✅ Table created successfully!\n")
            print("="*70)
            print("📊 Table: coding_question_bank")
            print("="*70)
            print("Columns:")
            for column in CodingQuestionBank.__table__.columns:
                print(f"  - {column.name}: {column.type}")
            print("="*70 + "\n")
            
            print("🎉 Question bank table is ready for use!\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    create_question_bank_table()
