"""
Piston API Client
Handles code execution via free Piston API
"""

import requests
import time
from typing import Dict, List, Optional, Tuple

# Piston API Configuration
PISTON_API = "https://emkc.org/api/v2/piston"

# Piston Language mapping
LANGUAGE_MAP = {
    'python': 'python',
    'javascript': 'javascript',
    'java': 'java',
    'cpp': 'c++',
    'c++': 'c++',
}

# Status mapping for consistency
STATUS_DESCRIPTIONS = {
    'success': "Accepted",
    'error': "Runtime Error",
    'timeout': "Time Limit Exceeded",
    'compilation_error': "Compilation Error"
}


def get_language_name(language: str) -> Optional[str]:
    """Get Piston language name from language identifier"""
    return LANGUAGE_MAP.get(language.lower())


def execute_code_simple(code: str, language: str, stdin: str = "") -> Tuple[bool, Dict]:
    """
    Execute code using Piston API
    
    Args:
        code: Source code to execute
        language: Programming language (python, javascript, java, cpp)
        stdin: Standard input for the program
    
    Returns:
        Tuple of (success: bool, result: dict)
    """
    piston_language = get_language_name(language)
    if not piston_language:
        print(f"❌ Unsupported language: {language}")
        return False, {'error': f'Unsupported language: {language}'}
    
    try:
        response = requests.post(
            f"{PISTON_API}/execute",
            json={
                "language": piston_language,
                "version": "*",  # Use latest version
                "files": [
                    {
                        "content": code
                    }
                ],
                "stdin": stdin
            },
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Piston API error: {response.status_code}")
            return False, {'error': f'API error: {response.status_code}'}
        
        data = response.json()
        run_data = data.get('run', {})
        
        stdout = run_data.get('stdout', '')
        stderr = run_data.get('stderr', '')
        exit_code = run_data.get('code', 0)
        
        # Determine success
        success = (exit_code == 0 and not stderr)
        
        result = {
            'stdout': stdout,
            'stderr': stderr,
            'exit_code': exit_code,
            'output': run_data.get('output', ''),
            'language': piston_language
        }
        
        if success:
            print(f"✅ Code executed successfully")
        else:
            print(f"❌ Code execution failed with exit code {exit_code}")
        
        return success, result
        
    except requests.exceptions.Timeout:
        print(f"⏰ Code execution timed out")
        return False, {'error': 'Execution timed out (10s limit)'}
    except Exception as e:
        print(f"❌ Error executing code: {str(e)}")
        return False, {'error': f'Execution failed: {str(e)}'}


def execute_code(code: str, language: str, stdin: str = "") -> Tuple[bool, Dict]:
    """
    Execute code and return results (main function)
    
    Args:
        code: Source code to execute
        language: Programming language
        stdin: Standard input
    
    Returns:
        Tuple of (success: bool, result: dict)
    """
    return execute_code_simple(code, language, stdin)


def run_test_cases(code: str, language: str, test_cases: List[Dict]) -> List[Dict]:
    """
    Run code against multiple test cases
    
    Args:
        code: Source code to execute
        language: Programming language
        test_cases: List of test cases [{"input": "...", "expected_output": "...", "is_hidden": bool}]
    
    Returns:
        List of test results with pass/fail status
    """
    results = []
    
    for idx, test_case in enumerate(test_cases):
        test_input = test_case.get('input', '')
        expected_output = test_case.get('expected_output', '').strip()
        is_hidden = test_case.get('is_hidden', False)
        
        print(f"\n🧪 Running test case {idx + 1}/{len(test_cases)}")
        
        # Wrap code to call function and print result
        wrapped_code = wrap_code_for_execution(code, language, test_input)
        
        # Execute code
        success, result = execute_code_simple(wrapped_code, language, "")
        
        if not success and result.get('error'):
            # Execution failed
            results.append({
                'test_case_id': idx + 1,
                'passed': False,
                'input': test_input if not is_hidden else '[Hidden]',
                'expected_output': expected_output if not is_hidden else '[Hidden]',
                'actual_output': '',
                'error': result.get('error', 'Unknown error'),
                'status': 'Runtime Error',
                'is_hidden': is_hidden
            })
            print(f"   ❌ FAILED: Test case {idx + 1} - {result.get('error', 'Unknown error')}")
            continue
        
        # Get actual output
        actual_output = result.get('stdout', '').strip()
        stderr = result.get('stderr', '').strip()
        
        # Determine status
        if stderr:
            status = 'Runtime Error'
            passed = False
        elif actual_output == expected_output:
            status = 'Accepted'
            passed = True
        else:
            status = 'Wrong Answer'
            passed = False
        
        # Build result
        test_result = {
            'test_case_id': idx + 1,
            'passed': passed,
            'input': test_input if not is_hidden else '[Hidden]',
            'expected_output': expected_output if not is_hidden else '[Hidden]',
            'actual_output': actual_output if not is_hidden else '[Hidden]',
            'status': status,
            'is_hidden': is_hidden
        }
        
        # Add error details if any
        if stderr:
            test_result['stderr'] = stderr if not is_hidden else '[Hidden]'
        
        results.append(test_result)
        
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'}: Test case {idx + 1}")
    
    return results


def wrap_code_for_execution(user_code: str, language: str, test_input: str) -> str:
    """
    Wrap user code with test harness to parse input and print output
    
    Args:
        user_code: User's function code
        language: Programming language
        test_input: Input string (e.g., "[2,7,11,15]\n9")
    
    Returns:
        Wrapped code ready for execution
    """
    if language == 'python':
        # For Python: Parse input, call function, print result
        return f"""{user_code}

# Test harness
import json
import sys

try:
    lines = '''{test_input}'''.strip().split('\\n')
    args = [json.loads(line) for line in lines]
    
    # Get function name from user code
    import re
    match = re.search(r'def\\s+(\\w+)\\s*\\(', '''{user_code}''')
    if match:
        func_name = match.group(1)
        result = globals()[func_name](*args)
        print(json.dumps(result, separators=(',', ':')))
    else:
        print("Error: No function found", file=sys.stderr)
except Exception as e:
    print(f"Error: {{e}}", file=sys.stderr)
"""
    
    elif language == 'javascript':
        # For JavaScript: Parse input, call function, print result
        return f"""{user_code}

// Test harness
try {{
    const lines = `{test_input}`.trim().split('\\n');
    const args = lines.map(line => JSON.parse(line));
    
    // Get function name
    const match = `{user_code}`.match(/function\\s+(\\w+)\\s*\\(/);
    if (match) {{
        const funcName = match[1];
        const result = eval(funcName)(...args);
        console.log(JSON.stringify(result));
    }} else {{
        console.error("Error: No function found");
    }}
}} catch (e) {{
    console.error(`Error: ${{e.message}}`);
}}
"""
    
    else:
        # For other languages, return as-is for now
        return user_code


def get_language_id(language: str) -> Optional[str]:
    """
    Get language identifier (for compatibility with existing code)
    
    Args:
        language: Programming language name
    
    Returns:
        Language name if supported, None otherwise
    """
    return get_language_name(language)


def validate_api() -> bool:
    """
    Validate that Piston API is accessible
    
    Returns:
        True if API is accessible, False otherwise
    """
    try:
        # Test with a simple Python code execution
        test_code = "print('Hello, World!')"
        success, result = execute_code_simple(test_code, "python", "")
        
        if success and result.get('stdout', '').strip() == 'Hello, World!':
            print("✅ Piston API is accessible and working")
            return True
        
        print("❌ Piston API validation failed")
        return False
        
    except Exception as e:
        print(f"❌ Error validating Piston API: {str(e)}")
        return False
