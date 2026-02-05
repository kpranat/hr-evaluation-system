"""
Code Execution Routes
Handles coding problem retrieval, code execution, and submission
"""

from flask import request, jsonify
from . import CodeExecution
from ..models import CodingProblem, CodingSubmission, CandidateAuth, CodingConfiguration
from ..extensions import db
from ..config import Config
from ..auth_helpers import verify_candidate_token, verify_recruiter_token
from .piston_client import execute_code, run_test_cases, get_language_id
import jwt
import os
from datetime import datetime


@CodeExecution.route('/config', methods=['GET'])
def get_coding_config():
    """
    GET CODING CONFIGURATION
    
    Get the coding round configuration (problems count, time limit, allowed languages)
    Uses default if no recruiter-specific config exists
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "config": {
                "problems_count": 3,
                "time_limit_minutes": 60,
                "allowed_languages": ["python", "javascript", "java", "cpp"]
            }
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    try:
        # Get default configuration (you can later make this recruiter-specific)
        config = CodingConfiguration.query.filter_by(is_active=True).first()
        
        if not config:
            # Return default values
            return jsonify({
                'success': True,
                'config': {
                    'problems_count': 3,
                    'time_limit_minutes': 60,
                    'allowed_languages': ['python', 'javascript', 'java', 'cpp']
                }
            }), 200
        
        return jsonify({
            'success': True,
            'config': config.to_dict()
        }), 200
        
    except Exception as e:
        print(f"\n❌ GET CONFIG ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/problems', methods=['GET'])
def get_coding_problems():
    """
    GET CODING PROBLEMS
    
    Fetches all coding problems for the candidate
    Returns problems without hidden test cases
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "problems": [
                {
                    "id": 1,
                    "problem_id": 1,
                    "title": "Two Sum",
                    "difficulty": "Easy",
                    "status": "not_attempted"  // or "attempted", "accepted"
                }
            ]
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    try:
        print(f"\n✅ Getting problems for candidate_id: {candidate_id}")
        
        # Get all problems
        problems = CodingProblem.query.all()
        print(f"✅ Found {len(problems)} problems")
        
        # Get candidate's submissions to determine status
        submissions = CodingSubmission.query.filter_by(candidate_id=candidate_id).all()
        print(f"✅ Found {len(submissions)} submissions for candidate")
        
        submission_map = {}
        
        for sub in submissions:
            if sub.problem_id not in submission_map:
                submission_map[sub.problem_id] = sub.status
            elif sub.status == 'Accepted':
                submission_map[sub.problem_id] = 'Accepted'
        
        problems_data = []
        for problem in problems:
            problem_dict = {
                'id': problem.id,
                'problem_id': problem.problem_id,
                'title': problem.title,
                'difficulty': problem.difficulty,
                'status': 'not_attempted'
            }
            
            # Determine status
            if problem.problem_id in submission_map:
                if submission_map[problem.problem_id] == 'Accepted':
                    problem_dict['status'] = 'accepted'
                else:
                    problem_dict['status'] = 'attempted'
            
            problems_data.append(problem_dict)
        
        return jsonify({
            'success': True,
            'problems': problems_data
        }), 200
        
    except Exception as e:
        print(f"\n❌ GET PROBLEMS ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/problems/<int:problem_id>', methods=['GET'])
def get_problem_detail(problem_id):
    """
    GET PROBLEM DETAILS
    
    Fetches full problem details including description, test cases, and starter code
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "problem": {
                "id": 1,
                "problem_id": 1,
                "title": "Two Sum",
                "description": "...",
                "difficulty": "Easy",
                "starter_code_python": "...",
                "test_cases": [...],  // Only visible test cases
                "hidden_test_cases_count": 1,
                "time_limit": 1000,
                "memory_limit": 128
            }
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    try:
        problem = CodingProblem.query.filter_by(problem_id=problem_id).first()
        
        if not problem:
            return jsonify({
                'success': False,
                'message': 'Problem not found'
            }), 404
        
        # Return problem without hidden test cases
        problem_dict = problem.to_dict(include_hidden=False)
        
        return jsonify({
            'success': True,
            'problem': problem_dict
        }), 200
        
    except Exception as e:
        print(f"\n❌ GET PROBLEM DETAIL ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/execute', methods=['POST'])
def execute_code_endpoint():
    """
    EXECUTE CODE
    
    Execute code against test cases and return results
    Does not save submission (use /submit for that)
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Request:
        {
            "code": "def twoSum(nums, target): ...",
            "language": "python",
            "problem_id": 1
        }
    
    Response:
        Success (200):
        {
            "success": true,
            "test_results": [
                {
                    "test_case_id": 1,
                    "passed": true,
                    "input": "[2,7,11,15]\\n9",
                    "expected_output": "[0,1]",
                    "actual_output": "[0,1]",
                    "status": "Accepted",
                    "time": "0.023",
                    "memory": "12345"
                }
            ],
            "passed_count": 2,
            "total_count": 3
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    data = request.json
    code = data.get('code')
    language = data.get('language', 'python')
    problem_id = data.get('problem_id')
    
    if not code:
        return jsonify({
            'success': False,
            'message': 'Code is required'
        }), 400
    
    if not problem_id:
        return jsonify({
            'success': False,
            'message': 'Problem ID is required'
        }), 400
    
    try:
        # Get problem with test cases
        problem = CodingProblem.query.filter_by(problem_id=problem_id).first()
        
        if not problem:
            return jsonify({
                'success': False,
                'message': 'Problem not found'
            }), 404
        
        # Validate language
        if not get_language_id(language):
            return jsonify({
                'success': False,
                'message': f'Unsupported language: {language}'
            }), 400
        
        # Get test cases
        test_cases = problem.test_cases_json or []
        
        if not test_cases:
            return jsonify({
                'success': False,
                'message': 'No test cases found for this problem'
            }), 400
        
        print(f"\n🚀 Executing code for problem {problem_id} in {language}")
        print(f"📊 Running {len(test_cases)} test cases...")
        
        # Run test cases
        test_results = run_test_cases(code, language, test_cases)
        
        # Calculate statistics
        passed_count = sum(1 for result in test_results if result['passed'])
        total_count = len(test_results)
        
        print(f"✅ Passed: {passed_count}/{total_count}")
        
        return jsonify({
            'success': True,
            'test_results': test_results,
            'passed_count': passed_count,
            'total_count': total_count
        }), 200
        
    except Exception as e:
        print(f"\n❌ EXECUTE CODE ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Execution failed: {str(e)}'
        }), 500


@CodeExecution.route('/submit', methods=['POST'])
def submit_solution():
    """
    SUBMIT SOLUTION
    
    Submit final solution for a problem
    Executes against all test cases and saves to database
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Request:
        {
            "problem_id": 1,
            "code": "def twoSum(nums, target): ...",
            "language": "python"
        }
    
    Response:
        Success (200):
        {
            "success": true,
            "submission_id": 1,
            "status": "Accepted",  // or "Wrong Answer", etc.
            "passed_count": 3,
            "total_count": 3,
            "test_results": [...]
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    data = request.json
    problem_id = data.get('problem_id')
    code = data.get('code')
    language = data.get('language', 'python')
    
    if not problem_id or not code:
        return jsonify({
            'success': False,
            'message': 'Problem ID and code are required'
        }), 400
    
    try:
        # Get problem
        problem = CodingProblem.query.filter_by(problem_id=problem_id).first()
        
        if not problem:
            return jsonify({
                'success': False,
                'message': 'Problem not found'
            }), 404
        
        # Run test cases
        test_cases = problem.test_cases_json or []
        test_results = run_test_cases(code, language, test_cases)
        
        # Determine overall status
        passed_count = sum(1 for result in test_results if result['passed'])
        total_count = len(test_results)
        
        # Calculate score percentage
        score_percentage = (passed_count / total_count * 100) if total_count > 0 else 0.0
        
        # Determine status - Always accept submission but mark appropriately
        if passed_count == total_count:
            status = 'Accepted'
        elif passed_count == 0:
            # Check for specific error types
            error_statuses = [result.get('status', 'Wrong Answer') for result in test_results if not result['passed']]
            if any('Time Limit' in s for s in error_statuses):
                status = 'Time Limit Exceeded'
            elif any('Runtime Error' in s for s in error_statuses):
                status = 'Runtime Error'
            elif any('Compilation Error' in s for s in error_statuses):
                status = 'Compilation Error'
            else:
                status = 'Wrong Answer'
        else:
            # Partial pass
            status = f'Partial ({passed_count}/{total_count})'
        
        # Calculate average runtime and memory
        runtimes = [float(result.get('time', 0) or 0) for result in test_results if result.get('time')]
        memories = [int(result.get('memory', 0) or 0) for result in test_results if result.get('memory')]
        
        avg_runtime = int(sum(runtimes) / len(runtimes) * 1000) if runtimes else None  # Convert to ms
        avg_memory = int(sum(memories) / len(memories)) if memories else None
        
        # Save submission - Always save regardless of pass/fail
        submission = CodingSubmission(
            candidate_id=candidate_id,
            problem_id=problem_id,
            code=code,
            language=language,
            status=status,
            passed_test_cases=passed_count,
            total_test_cases=total_count,
            score_percentage=score_percentage,
            test_results_json=test_results,
            runtime=avg_runtime,
            memory_usage=avg_memory
        )
        
        db.session.add(submission)
        db.session.commit()
        
        print(f"✅ Submission saved: ID={submission.id}, Status={status}, Score={score_percentage:.1f}% ({passed_count}/{total_count})")
        
        return jsonify({
            'success': True,
            'submission_id': submission.id,
            'score_percentage': score_percentage,
            'status': status,
            'passed_count': passed_count,
            'total_count': total_count,
            'test_results': test_results,
            'runtime': avg_runtime,
            'memory_usage': avg_memory
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ SUBMIT SOLUTION ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Submission failed: {str(e)}'
        }), 500


@CodeExecution.route('/submissions/<int:problem_id>', methods=['GET'])
def get_submission_history(problem_id):
    """
    GET SUBMISSION HISTORY
    
    Get all submissions for a specific problem by the candidate
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "submissions": [
                {
                    "id": 1,
                    "code": "...",
                    "language": "python",
                    "status": "Accepted",
                    "runtime": 23,
                    "memory_usage": 12345,
                    "submitted_at": "2026-02-05T10:30:00"
                }
            ]
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    try:
        submissions = CodingSubmission.query.filter_by(
            candidate_id=candidate_id,
            problem_id=problem_id
        ).order_by(CodingSubmission.submitted_at.desc()).all()
        
        submissions_data = [sub.to_dict() for sub in submissions]
        
        return jsonify({
            'success': True,
            'submissions': submissions_data
        }), 200
        
    except Exception as e:
        print(f"\n❌ GET SUBMISSION HISTORY ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/complete', methods=['POST'])
def complete_coding_round():
    """
    COMPLETE CODING ROUND
    
    Mark the coding round as completed for the candidate
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "message": "Coding round completed successfully"
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    try:
        candidate = CandidateAuth.query.get(candidate_id)
        
        if not candidate:
            return jsonify({
                'success': False,
                'message': 'Candidate not found'
            }), 404
        
        # Mark as completed (allow recompletion for testing)
        candidate.coding_completed = True
        candidate.coding_completed_at = datetime.utcnow()
        
        db.session.commit()
        
        print(f"✅ Coding round completed for candidate {candidate_id}")
        
        return jsonify({
            'success': True,
            'message': 'Coding round completed successfully',
            'completed_at': candidate.coding_completed_at.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ COMPLETE CODING ROUND ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/status', methods=['GET'])
def get_coding_status():
    """
    GET CODING ROUND STATUS
    
    Get the candidate's coding round status and progress
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "status": {
                "coding_completed": false,
                "coding_completed_at": null,
                "problems_attempted": 2,
                "problems_accepted": 1,
                "total_submissions": 5
            }
        }
    """
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    try:
        candidate = CandidateAuth.query.get(candidate_id)
        
        if not candidate:
            return jsonify({
                'success': False,
                'message': 'Candidate not found'
            }), 404
        
        # Get submission statistics
        submissions = CodingSubmission.query.filter_by(candidate_id=candidate_id).all()
        
        # Calculate statistics
        attempted_problems = set(sub.problem_id for sub in submissions)
        accepted_problems = set(sub.problem_id for sub in submissions if sub.status == 'Accepted')
        
        return jsonify({
            'success': True,
            'status': {
                'coding_completed': candidate.coding_completed,
                'coding_completed_at': candidate.coding_completed_at.isoformat() if candidate.coding_completed_at else None,
                'problems_attempted': len(attempted_problems),
                'problems_accepted': len(accepted_problems),
                'total_submissions': len(submissions)
            }
        }), 200
        
    except Exception as e:
        print(f"\n❌ GET CODING STATUS ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


# ==================== ADMIN ROUTES ====================

@CodeExecution.route('/admin/problems', methods=['GET'])
def get_all_problems_admin():
    """
    GET ALL CODING PROBLEMS (ADMIN)
    
    Get list of all coding problems for recruiter management
    
    Authentication: Required (JWT Bearer token - recruiter only)
    
    Response:
        Success (200):
        {
            "success": true,
            "problems": [...]
        }
    """
    recruiter_id, error_response = verify_recruiter_token()
    if error_response:
        return error_response
    
    try:
        problems = CodingProblem.query.order_by(CodingProblem.created_at.desc()).all()
        
        problems_data = []
        for problem in problems:
            problems_data.append({
                'problem_id': problem.problem_id,
                'title': problem.title,
                'description': problem.description,
                'difficulty': problem.difficulty,
                'test_cases_count': len(problem.test_cases_json) if problem.test_cases_json else 0,
                'created_at': problem.created_at.isoformat() if problem.created_at else None
            })
        
        return jsonify({
            'success': True,
            'problems': problems_data
        }), 200
        
    except Exception as e:
        print(f"\n❌ GET ADMIN PROBLEMS ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/admin/problems', methods=['POST'])
def create_problem_admin():
    """
    CREATE CODING PROBLEM (ADMIN)
    
    Create a new coding problem
    
    Authentication: Required (JWT Bearer token - recruiter only)
    
    Request:
        {
            "title": "Two Sum",
            "description": "...",
            "difficulty": "easy",
            "starter_code_python": "...",
            "starter_code_javascript": "...",
            "starter_code_java": "...",
            "starter_code_cpp": "...",
            "test_cases": [
                {
                    "input": "[2,7,11,15]\\n9",
                    "expected_output": "[0,1]",
                    "is_hidden": false
                }
            ],
            "time_limit_seconds": 5,
            "memory_limit_mb": 256
        }
    
    Response:
        Success (201):
        {
            "success": true,
            "problem_id": 1,
            "message": "Problem created successfully"
        }
    """
    recruiter_id, error_response = verify_recruiter_token()
    if error_response:
        return error_response
    
    data = request.json
    
    try:
        # Validate required fields
        if not data.get('title'):
            return jsonify({
                'success': False,
                'message': 'Title is required'
            }), 400
        
        if not data.get('description'):
            return jsonify({
                'success': False,
                'message': 'Description is required'
            }), 400
        
        if not data.get('test_cases') or len(data.get('test_cases')) == 0:
            return jsonify({
                'success': False,
                'message': 'At least one test case is required'
            }), 400
        
        # Generate problem_id (use max + 1 or 1 if no problems exist)
        max_problem = CodingProblem.query.order_by(CodingProblem.problem_id.desc()).first()
        next_problem_id = (max_problem.problem_id + 1) if max_problem else 1
        
        # Create new problem
        new_problem = CodingProblem(
            problem_id=next_problem_id,
            title=data.get('title'),
            description=data.get('description'),
            difficulty=data.get('difficulty', 'medium'),
            starter_code_python=data.get('starter_code_python', ''),
            starter_code_javascript=data.get('starter_code_javascript', ''),
            starter_code_java=data.get('starter_code_java', ''),
            starter_code_cpp=data.get('starter_code_cpp', ''),
            test_cases_json=data.get('test_cases'),
            time_limit=data.get('time_limit_seconds', 5) * 1000 if 'time_limit_seconds' in data else data.get('time_limit', 5000),
            memory_limit=data.get('memory_limit_mb', 256) if 'memory_limit_mb' in data else data.get('memory_limit', 256)
        )
        
        db.session.add(new_problem)
        db.session.commit()
        
        print(f"✅ Created new coding problem: {new_problem.title} (ID: {new_problem.problem_id})")
        
        return jsonify({
            'success': True,
            'problem_id': new_problem.problem_id,
            'message': 'Problem created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ CREATE PROBLEM ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/admin/import/scan', methods=['GET'])
def scan_sample_problems():
    """
    SCAN SAMPLE PROBLEMS
    
    Scan the sample problems folder and return available questions
    
    Authentication: Required (JWT Bearer token - recruiter only)
    
    Response:
        Success (200):
        {
            "success": true,
            "problems": [
                {
                    "file_path": "...",
                    "title": "Two Sum",
                    "category": "Arrays",
                    "difficulty": "easy",
                    "test_cases_count": 3
                }
            ],
            "total": 150
        }
    """
    recruiter_id, error_response = verify_recruiter_token()
    if error_response:
        return error_response
    
    try:
        from .problem_parser import scan_sample_problems
        import os
        
        # Get path to sample problems
        base_dir = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 
            'CODING SAMPLE QUESTIONS', 
            'coding-problems'
        )
        
        if not os.path.exists(base_dir):
            return jsonify({
                'success': False,
                'message': 'Sample problems folder not found'
            }), 404
        
        # Scan problems
        problems = scan_sample_problems(base_dir)
        
        # Format for response
        formatted_problems = []
        for problem in problems:
            formatted_problems.append({
                'file_path': problem['file_path'],
                'title': problem['title'],
                'category': problem['category'],
                'difficulty': problem['difficulty'],
                'test_cases_count': len(problem['test_cases']),
                'description_preview': problem['description'][:100] + '...' if len(problem['description']) > 100 else problem['description']
            })
        
        # Group by category
        categories = {}
        for problem in formatted_problems:
            cat = problem['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(problem)
        
        return jsonify({
            'success': True,
            'problems': formatted_problems,
            'categories': categories,
            'total': len(formatted_problems)
        }), 200
        
    except Exception as e:
        print(f"\n❌ SCAN PROBLEMS ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@CodeExecution.route('/admin/import/batch', methods=['POST'])
def import_batch_problems():
    """
    IMPORT BATCH PROBLEMS
    
    Import selected problems from sample files into the database
    
    Authentication: Required (JWT Bearer token - recruiter only)
    
    Request Body:
        {
            "file_paths": ["path1.py", "path2.py"]
        }
    
    Response:
        Success (200):
        {
            "success": true,
            "imported": 5,
            "failed": 1,
            "errors": ["Error message for failed import"],
            "message": "Imported 5 out of 6 problems"
        }
    """
    recruiter_id, error_response = verify_recruiter_token()
    if error_response:
        return error_response
    
    data = request.json
    file_paths = data.get('file_paths', [])
    
    if not file_paths:
        return jsonify({
            'success': False,
            'message': 'No file paths provided'
        }), 400
    
    try:
        from .problem_parser import parse_python_problem_file, format_problem_for_db
        
        imported = 0
        failed = 0
        errors = []
        
        for file_path in file_paths:
            try:
                # Parse problem
                problem_data = parse_python_problem_file(file_path)
                
                if not problem_data:
                    failed += 1
                    errors.append(f"Failed to parse {os.path.basename(file_path)}")
                    continue
                
                # Check if problem already exists
                existing = CodingProblem.query.filter_by(title=problem_data['title']).first()
                if existing:
                    failed += 1
                    errors.append(f"Problem '{problem_data['title']}' already exists")
                    continue
                
                # Generate problem_id
                max_problem = CodingProblem.query.order_by(CodingProblem.problem_id.desc()).first()
                next_problem_id = (max_problem.problem_id + 1) if max_problem else 1
                
                # Format for database
                db_data = format_problem_for_db(problem_data)
                db_data['problem_id'] = next_problem_id
                
                # Create new problem
                new_problem = CodingProblem(**db_data)
                db.session.add(new_problem)
                imported += 1
                
                # Update max for next iteration
                max_problem = new_problem
                
            except Exception as e:
                failed += 1
                errors.append(f"Error importing {os.path.basename(file_path)}: {str(e)}")
        
        # Commit all imports
        db.session.commit()
        
        print(f"✅ Imported {imported} problems, {failed} failed")
        
        return jsonify({
            'success': True,
            'imported': imported,
            'failed': failed,
            'errors': errors,
            'message': f'Imported {imported} out of {len(file_paths)} problems'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ BATCH IMPORT ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500
