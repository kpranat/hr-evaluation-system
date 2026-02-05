"""
Parse coding problems from sample questions folder
Extracts problem descriptions, test cases, and starter code
"""
import os
import re
import ast
from typing import List, Dict, Optional, Tuple


def parse_python_problem_file(file_path: str) -> Optional[Dict]:
    """
    Parse a Python problem file to extract:
    - Problem title
    - Problem description
    - Test cases (input/output)
    - Function signature
    
    Args:
        file_path: Path to the Python file
    
    Returns:
        Dict with problem details or None if parsing fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract docstring (problem description)
        docstring_match = re.search(r"'''(.*?)'''", content, re.DOTALL)
        if not docstring_match:
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        
        if not docstring_match:
            print(f"⚠️  No docstring found in {file_path}")
            return None
        
        docstring = docstring_match.group(1).strip()
        
        # Extract title (first line of docstring)
        lines = docstring.split('\n')
        title = lines[0].strip()
        
        # Extract description (everything before "Input:")
        description_parts = []
        for line in lines[1:]:
            if line.strip().startswith('Input:') or line.strip().startswith('========='):
                break
            if line.strip():
                description_parts.append(line.strip())
        
        description = '\n'.join(description_parts)
        
        # Extract examples from docstring
        examples = []
        for i, line in enumerate(lines):
            if line.strip().startswith('Input:'):
                input_val = line.replace('Input:', '').strip()
                # Look for Output in next lines
                for j in range(i+1, len(lines)):
                    if lines[j].strip().startswith('Output:'):
                        output_val = lines[j].replace('Output:', '').strip()
                        examples.append({
                            'input': input_val,
                            'output': output_val
                        })
                        break
        
        # Extract function signature
        function_match = re.search(r'def\s+(\w+)\s*\((.*?)\):', content)
        if not function_match:
            print(f"⚠️  No function found in {file_path}")
            return None
        
        function_name = function_match.group(1)
        params = function_match.group(2).strip()
        
        # Extract test cases from the Testing section
        test_cases = []
        testing_section = content.split('# Testing #')
        if len(testing_section) > 1:
            test_code = testing_section[1]
            
            # Find print statements with function calls
            print_matches = re.findall(
                rf'print\({function_name}\((.*?)\)\)',
                test_code,
                re.DOTALL
            )
            
            # Find commented expected results
            comment_matches = re.findall(
                r'# Correct result => (.*?)$',
                test_code,
                re.MULTILINE
            )
            
            for i, (input_str, expected) in enumerate(zip(print_matches, comment_matches)):
                # Clean input
                input_clean = input_str.strip()
                expected_clean = expected.strip()
                
                test_cases.append({
                    'input': input_clean,
                    'expected_output': expected_clean,
                    'is_hidden': i >= 2  # First 2 visible, rest hidden
                })
        
        # If no test cases from Testing section, use examples from docstring
        if not test_cases and examples:
            for i, example in enumerate(examples):
                test_cases.append({
                    'input': example['input'],
                    'expected_output': example['output'],
                    'is_hidden': i >= 2
                })
        
        # Determine difficulty based on folder or complexity hints
        difficulty = 'medium'  # default
        if 'easy' in file_path.lower() or 'simple' in description.lower():
            difficulty = 'easy'
        elif 'hard' in file_path.lower() or 'difficult' in description.lower() or 'Dynamic Programming' in file_path:
            difficulty = 'hard'
        
        # Generate starter code template
        if params:
            param_list = [p.strip().split('=')[0].strip() for p in params.split(',')]
            starter_code_python = f"def {function_name}({params}):\n    # Write your code here\n    pass"
        else:
            starter_code_python = f"def {function_name}():\n    # Write your code here\n    pass"
        
        # Extract folder/category
        category = os.path.basename(os.path.dirname(file_path))
        
        return {
            'file_path': file_path,
            'title': title,
            'description': description,
            'category': category,
            'difficulty': difficulty,
            'function_name': function_name,
            'params': params,
            'starter_code_python': starter_code_python,
            'test_cases': test_cases,
            'examples': examples
        }
        
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {str(e)}")
        return None


def scan_sample_problems(base_dir: str) -> List[Dict]:
    """
    Scan all Python files in the sample problems directory
    
    Args:
        base_dir: Base directory containing problem folders
    
    Returns:
        List of parsed problems
    """
    problems = []
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                problem = parse_python_problem_file(file_path)
                if problem:
                    problems.append(problem)
    
    print(f"\n✅ Scanned {len(problems)} problems from {base_dir}")
    return problems


def format_problem_for_db(problem: Dict) -> Dict:
    """
    Format parsed problem for database insertion
    
    Args:
        problem: Parsed problem dict
    
    Returns:
        Formatted dict ready for CodingProblem model
    """
    return {
        'title': problem['title'],
        'description': f"{problem['description']}\n\nCategory: {problem['category']}",
        'difficulty': problem['difficulty'],
        'starter_code_python': problem['starter_code_python'],
        'starter_code_javascript': '',  # Can be generated later
        'starter_code_java': '',
        'starter_code_cpp': '',
        'test_cases_json': problem['test_cases'],
        'time_limit': 5000,  # 5 seconds in milliseconds
        'memory_limit': 256  # 256 MB
    }


if __name__ == '__main__':
    # Test the parser
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'CODING SAMPLE QUESTIONS', 'coding-problems')
    print(f"Scanning directory: {os.path.abspath(base_dir)}")
    
    if not os.path.exists(base_dir):
        print(f"❌ Directory not found: {base_dir}")
    else:
        problems = scan_sample_problems(base_dir)
        
        if problems:
            print(f"\n📝 Sample problem #1:")
            print(f"Title: {problems[0]['title']}")
            print(f"Category: {problems[0]['category']}")
            print(f"Difficulty: {problems[0]['difficulty']}")
            print(f"Function: {problems[0]['function_name']}({problems[0]['params']})")
            print(f"Test Cases: {len(problems[0]['test_cases'])}")
            if problems[0]['test_cases']:
                print(f"\nFirst Test Case:")
                print(f"  Input: {problems[0]['test_cases'][0]['input']}")
                print(f"  Expected: {problems[0]['test_cases'][0]['expected_output']}")
            print(f"\nStarter Code:\n{problems[0]['starter_code_python']}")
