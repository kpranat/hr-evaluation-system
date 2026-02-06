"""
Coding Problems Supabase Service
Handles CRUD operations for active coding problems in Supabase
"""

from typing import List, Dict, Optional
from .supabase_client import get_supabase


class CodingProblemsSupabaseService:
    """Service for managing active coding problems in Supabase"""
    
    TABLE_NAME = 'coding_problems'
    
    @staticmethod
    def get_all_problems() -> List[Dict]:
        """
        Get all active coding problems
        
        Returns:
            List of problem dictionaries
        """
        try:
            supabase = get_supabase()
            response = supabase.table(CodingProblemsSupabaseService.TABLE_NAME)\
                .select('*')\
                .order('problem_id')\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Error fetching problems: {str(e)}")
            raise
    
    @staticmethod
    def get_problem_by_id(problem_id: int) -> Optional[Dict]:
        """
        Get a specific problem by problem_id
        
        Args:
            problem_id: The ID of the problem
            
        Returns:
            Problem dictionary or None if not found
        """
        try:
            supabase = get_supabase()
            response = supabase.table(CodingProblemsSupabaseService.TABLE_NAME)\
                .select('*')\
                .eq('problem_id', problem_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error fetching problem {problem_id}: {str(e)}")
            raise
    
    @staticmethod
    def create_problem(problem_data: Dict) -> Dict:
        """
        Create a new active problem
        
        Args:
            problem_data: Dictionary containing problem details
            
        Returns:
            Created problem dictionary
        """
        try:
            supabase = get_supabase()
            
            # Prepare data for insertion
            insert_data = {
                'problem_id': problem_data['problem_id'],
                'title': problem_data['title'],
                'description': problem_data['description'],
                'difficulty': problem_data.get('difficulty', 'medium'),
                'starter_code_python': problem_data.get('starter_code_python', ''),
                'starter_code_javascript': problem_data.get('starter_code_javascript', ''),
                'starter_code_java': problem_data.get('starter_code_java', ''),
                'starter_code_cpp': problem_data.get('starter_code_cpp', ''),
                'test_cases': problem_data.get('test_cases', []),
                'time_limit_seconds': problem_data.get('time_limit_seconds', 5),
                'memory_limit_mb': problem_data.get('memory_limit_mb', 256),
                'category': problem_data.get('category', 'general'),
                'tags': problem_data.get('tags', [])
            }
            
            response = supabase.table(CodingProblemsSupabaseService.TABLE_NAME)\
                .insert(insert_data)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error creating problem: {str(e)}")
            raise
    
    @staticmethod
    def update_problem(problem_id: int, problem_data: Dict) -> Dict:
        """
        Update an existing problem
        
        Args:
            problem_id: The ID of the problem to update
            problem_data: Dictionary containing updated problem details
            
        Returns:
            Updated problem dictionary
        """
        try:
            supabase = get_supabase()
            
            response = supabase.table(CodingProblemsSupabaseService.TABLE_NAME)\
                .update(problem_data)\
                .eq('problem_id', problem_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error updating problem: {str(e)}")
            raise
    
    @staticmethod
    def delete_problem(problem_id: int) -> bool:
        """
        Delete a problem
        
        Args:
            problem_id: The ID of the problem to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            supabase = get_supabase()
            
            response = supabase.table(CodingProblemsSupabaseService.TABLE_NAME)\
                .delete()\
                .eq('problem_id', problem_id)\
                .execute()
            
            return True
        except Exception as e:
            print(f"❌ Error deleting problem: {str(e)}")
            raise
