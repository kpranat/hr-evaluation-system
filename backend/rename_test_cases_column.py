"""
Rename test_cases_json column to test_cases in local PostgreSQL

This script renames the column in the coding_question_bank table
to match the Supabase schema naming convention.

Usage:
    python rename_test_cases_column.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db


def rename_column():
    """Rename test_cases_json to test_cases in coding_question_bank table"""
    print("\n" + "="*70)
    print("🔄 RENAME COLUMN: test_cases_json → test_cases")
    print("="*70 + "\n")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if table exists
            inspector = db.inspect(db.engine)
            if 'coding_question_bank' not in inspector.get_table_names():
                print("ℹ️  Table 'coding_question_bank' does not exist")
                print("   Nothing to rename.\n")
                return
            
            # Check current columns
            columns = [col['name'] for col in inspector.get_columns('coding_question_bank')]
            
            if 'test_cases' in columns:
                print("✅ Column 'test_cases' already exists")
                print("   Migration already complete.\n")
                return
            
            if 'test_cases_json' not in columns:
                print("ℹ️  Column 'test_cases_json' does not exist")
                print("   Nothing to rename.\n")
                return
            
            # Rename the column
            print("📝 Renaming column 'test_cases_json' to 'test_cases'...")
            
            # Execute raw SQL to rename column (PostgreSQL syntax)
            db.session.execute(db.text(
                "ALTER TABLE coding_question_bank "
                "RENAME COLUMN test_cases_json TO test_cases"
            ))
            db.session.commit()
            
            print("✅ Column renamed successfully!\n")
            print("="*70)
            print("📊 Updated Table: coding_question_bank")
            print("="*70)
            
            # Show updated columns
            inspector = db.inspect(db.engine)
            columns = inspector.get_columns('coding_question_bank')
            print("Columns:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            print("="*70 + "\n")
            
            print("🎉 Migration complete!\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            db.session.rollback()
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    rename_column()
