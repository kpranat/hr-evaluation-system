"""
Coding Question Bank Service
Handles CRUD operations for the coding question bank in Supabase
"""

from typing import List, Dict, Optional
from .supabase_client import get_supabase


class CodingQuestionBankService:
    """Service for managing coding question bank in Supabase"""
    
    TABLE_NAME = 'coding_question_bank'
    
    @staticmethod
    def get_all_questions() -> List[Dict]:
        """
        Get all questions from the bank
        
        Returns:
            List of question dictionaries
        """
        try:
            supabase = get_supabase()
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .select('*')\
                .order('bank_id')\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Error fetching questions from bank: {str(e)}")
            raise
    
    @staticmethod
    def get_question_by_id(bank_id: int) -> Optional[Dict]:
        """
        Get a specific question by bank_id
        
        Args:
            bank_id: The bank ID of the question
            
        Returns:
            Question dictionary or None if not found
        """
        try:
            supabase = get_supabase()
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .select('*')\
                .eq('bank_id', bank_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error fetching question {bank_id} from bank: {str(e)}")
            raise
    
    @staticmethod
    def get_questions_by_category(category: str) -> List[Dict]:
        """
        Get questions by category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of question dictionaries
        """
        try:
            supabase = get_supabase()
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .select('*')\
                .eq('category', category)\
                .order('bank_id')\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Error fetching questions by category: {str(e)}")
            raise
    
    @staticmethod
    def create_question(question_data: Dict) -> Dict:
        """
        Create a new question in the bank
        
        Args:
            question_data: Dictionary containing question details
            
        Returns:
            Created question dictionary
        """
        try:
            supabase = get_supabase()
            
            # Prepare data for insertion
            insert_data = {
                'bank_id': question_data['bank_id'],
                'title': question_data['title'],
                'description': question_data['description'],
                'difficulty': question_data.get('difficulty', 'medium'),
                'starter_code_python': question_data.get('starter_code_python', ''),
                'starter_code_javascript': question_data.get('starter_code_javascript', ''),
                'starter_code_java': question_data.get('starter_code_java', ''),
                'starter_code_cpp': question_data.get('starter_code_cpp', ''),
                'test_cases': question_data.get('test_cases', []),
                'time_limit': question_data.get('time_limit', 5),
                'memory_limit': question_data.get('memory_limit', 256),
                'category': question_data.get('category', 'general'),
                'tags': question_data.get('tags', []),
                'source_file': question_data.get('source_file', '')
            }
            
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .insert(insert_data)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error creating question in bank: {str(e)}")
            raise
    
    @staticmethod
    def update_question(bank_id: int, question_data: Dict) -> Dict:
        """
        Update an existing question in the bank
        
        Args:
            bank_id: The bank ID of the question to update
            question_data: Dictionary containing updated question details
            
        Returns:
            Updated question dictionary
        """
        try:
            supabase = get_supabase()
            
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .update(question_data)\
                .eq('bank_id', bank_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error updating question in bank: {str(e)}")
            raise
    
    @staticmethod
    def delete_question(bank_id: int) -> bool:
        """
        Delete a question from the bank
        
        Args:
            bank_id: The bank ID of the question to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            supabase = get_supabase()
            
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .delete()\
                .eq('bank_id', bank_id)\
                .execute()
            
            return True
        except Exception as e:
            print(f"❌ Error deleting question from bank: {str(e)}")
            raise
    
    @staticmethod
    def question_exists(title: str) -> bool:
        """
        Check if a question with the given title already exists
        
        Args:
            title: Question title to check
            
        Returns:
            True if question exists
        """
        try:
            supabase = get_supabase()
            response = supabase.table(CodingQuestionBankService.TABLE_NAME)\
                .select('bank_id')\
                .eq('title', title)\
                .execute()
            
            return response.data and len(response.data) > 0
        except Exception as e:
            print(f"❌ Error checking question existence: {str(e)}")
            raise
