"""
Check what coding problems exist in the database
"""
from app import create_app
from app.models import CodingProblem
from app.extensions import db

app = create_app()

with app.app_context():
    problems = CodingProblem.query.all()
    
    print(f"\n{'='*60}")
    print(f"CODING PROBLEMS IN DATABASE: {len(problems)}")
    print(f"{'='*60}\n")
    
    if problems:
        for problem in problems:
            print(f"ID: {problem.problem_id}")
            print(f"Title: {problem.title}")
            print(f"Difficulty: {problem.difficulty}")
            print(f"Test Cases: {len(problem.test_cases_json) if problem.test_cases_json else 0}")
            print(f"Created: {problem.created_at}")
            print("-" * 60)
    else:
        print("No problems found in database")
    
    # Ask if user wants to clear
    print("\n" + "="*60)
    response = input("\nDo you want to delete all existing problems? (yes/no): ")
    
    if response.lower() == 'yes':
        for problem in problems:
            db.session.delete(problem)
        db.session.commit()
        print(f"✅ Deleted {len(problems)} problems from database")
    else:
        print("No changes made")
