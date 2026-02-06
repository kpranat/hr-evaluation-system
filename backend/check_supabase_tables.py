"""
Diagnostic Script: Check Supabase Tables

This script checks which tables exist in Supabase and how many records each has.
Use this to diagnose where your data actually is.

Usage:
    python check_supabase_tables.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.supabase_client import get_supabase


def check_tables():
    """Check Supabase tables and record counts"""
    print("\n" + "="*70)
    print("🔍 SUPABASE TABLE DIAGNOSTIC")
    print("="*70 + "\n")
    
    try:
        supabase = get_supabase()
        print("✅ Connected to Supabase\n")
        
        # Check coding_question_bank table
        print("-" * 70)
        print("📊 Table: coding_question_bank")
        print("-" * 70)
        try:
            response = supabase.table('coding_question_bank').select('id', count='exact').execute()
            count = len(response.data) if response.data else 0
            print(f"Records: {count}")
            if count > 0:
                print("✅ This table has data!")
                # Show sample
                sample = supabase.table('coding_question_bank').select('bank_id, title, difficulty').limit(3).execute()
                if sample.data:
                    print("\nSample records:")
                    for record in sample.data:
                        print(f"  - [{record.get('bank_id')}] {record.get('title')} ({record.get('difficulty')})")
            else:
                print("❌ This table is EMPTY")
        except Exception as e:
            print(f"❌ Error accessing table: {str(e)}")
            print("   Table might not exist")
        
        print("\n")
        
        # Check coding_problems table
        print("-" * 70)
        print("📊 Table: coding_problems")
        print("-" * 70)
        try:
            response = supabase.table('coding_problems').select('id', count='exact').execute()
            count = len(response.data) if response.data else 0
            print(f"Records: {count}")
            if count > 0:
                print("⚠️  This table has data (but it's not used by the import feature)")
                # Show sample
                sample = supabase.table('coding_problems').select('problem_id, title, difficulty').limit(3).execute()
                if sample.data:
                    print("\nSample records:")
                    for record in sample.data:
                        print(f"  - [{record.get('problem_id')}] {record.get('title')} ({record.get('difficulty')})")
            else:
                print("✅ This table is empty (as expected)")
        except Exception as e:
            print(f"❌ Error accessing table: {str(e)}")
            print("   Table might not exist")
        
        print("\n" + "="*70)
        print("📋 DIAGNOSIS")
        print("="*70)
        print("\nFor the import feature to work, you need:")
        print("  1. ✅ coding_question_bank table (with data)")
        print("  2. ❌ coding_problems table (not needed for import)")
        print("\nIf your data is in 'coding_problems', you need to:")
        print("  1. Create 'coding_question_bank' table with the correct schema")
        print("  2. Run the migration script: python migrate_question_bank.py")
        print("\nOr if you want to move existing data:")
        print("  - Use Supabase SQL Editor to copy data between tables")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_tables()
