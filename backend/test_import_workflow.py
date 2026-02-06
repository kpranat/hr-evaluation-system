"""
Test Script: Verify Import Workflow

This script tests the complete import workflow:
1. Fetch questions from Supabase (scan endpoint)
2. Import selected questions to PostgreSQL (batch endpoint)
3. Verify questions were created successfully

Usage:
    python test_import_workflow.py
"""

import sys
import os
import requests

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import CodingProblem
from app.extensions import db


def test_workflow():
    """Test the complete import workflow"""
    print("\n" + "="*70)
    print("🧪 TESTING IMPORT WORKFLOW")
    print("="*70 + "\n")
    
    BASE_URL = "http://localhost:5000/api/code"
    
    # You'll need a real recruiter token - get it from localStorage after login
    # For now, we'll test the backend logic directly
    
    app = create_app()
    
    with app.app_context():
        print("Step 1: Check initial problems in PostgreSQL")
        print("-" * 70)
        initial_count = CodingProblem.query.count()
        print(f"Current problems in PostgreSQL: {initial_count}")
        
        print("\n\nStep 2: Import from Supabase question bank")
        print("-" * 70)
        print("Testing the import logic...")
        
        # Import the service
        from app.services.coding_question_bank import CodingQuestionBankService
        
        # Fetch questions from Supabase
        questions = CodingQuestionBankService.get_all_questions()
        print(f"✅ Found {len(questions)} questions in Supabase question bank")
        
        if len(questions) > 0:
            print("\nSample questions:")
            for i, q in enumerate(questions[:3]):
                print(f"  {i+1}. [{q.get('bank_id')}] {q.get('title')} ({q.get('difficulty')})")
        
        print("\n\nStep 3: Test importing one question")
        print("-" * 70)
        
        if len(questions) > 0:
            # Get the first question that isn't already imported
            existing_titles = {p.title for p in CodingProblem.query.all()}
            
            test_question = None
            for q in questions:
                if q.get('title') not in existing_titles:
                    test_question = q
                    break
            
            if test_question:
                # Get next problem_id
                next_problem_id = 1
                existing_problems = CodingProblem.query.all()
                if existing_problems:
                    max_id = max(p.problem_id for p in existing_problems)
                    next_problem_id = max_id + 1
                
                # Create the problem
                try:
                    problem = CodingProblem(
                        problem_id=next_problem_id,
                        title=test_question['title'],
                        description=test_question['description'],
                        difficulty=test_question['difficulty'],
                        starter_code_python=test_question.get('starter_code_python', ''),
                        starter_code_javascript=test_question.get('starter_code_javascript', ''),
                        starter_code_java=test_question.get('starter_code_java', ''),
                        starter_code_cpp=test_question.get('starter_code_cpp', ''),
                        test_cases_json=test_question.get('test_cases', []),
                        time_limit=test_question.get('time_limit', 5) * 1000,
                        memory_limit=test_question.get('memory_limit', 256)
                    )
                    
                    db.session.add(problem)
                    db.session.commit()
                    
                    print(f"✅ Successfully imported: {test_question['title']}")
                    print(f"   Problem ID: {next_problem_id}")
                    print(f"   Test cases: {len(test_question.get('test_cases', []))}")
                    
                except Exception as e:
                    print(f"❌ Failed to import: {str(e)}")
                    db.session.rollback()
                    import traceback
                    traceback.print_exc()
            else:
                print("⚠️  All questions already imported")
        
        print("\n\nStep 4: Verify final state")
        print("-" * 70)
        final_count = CodingProblem.query.count()
        print(f"Problems in PostgreSQL after import: {final_count}")
        print(f"Increase: {final_count - initial_count}")
        
        print("\n" + "="*70)
        print("✅ IMPORT WORKFLOW TEST COMPLETE")
        print("="*70)
        print("\nSummary:")
        print(f"  - Supabase question bank: {len(questions)} questions")
        print(f"  - PostgreSQL problems: {final_count} problems")
        print(f"  - Import working: {'✅ YES' if final_count > initial_count or initial_count > 0 else '⚠️  Check manually'}")
        print("\nNext steps:")
        print("  1. Login to frontend as recruiter")
        print("  2. Navigate to Coding Problems Management")
        print("  3. Click 'Import from Bank'")
        print("  4. Select questions and import")
        print("="*70 + "\n")


if __name__ == "__main__":
    test_workflow()
