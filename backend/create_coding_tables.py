"""
Database Migration Script for Coding Round
Creates tables for coding problems, submissions, and configuration
Adds coding_completed fields to candidate_auth table
"""

import psycopg2
from psycopg2.extras import Json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL)

def migrate_candidate_auth_table():
    """Add coding completion columns to candidate_auth table"""
    print("\n🔧 Checking candidate_auth table for coding columns...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='candidate_auth' 
            AND column_name IN ('coding_completed', 'coding_completed_at');
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        if 'coding_completed' in existing_columns and 'coding_completed_at' in existing_columns:
            print("✅ Coding columns already exist in candidate_auth table")
            cursor.close()
            conn.close()
            return True
        
        # Add columns if they don't exist
        print("📝 Adding coding columns to candidate_auth table...")
        
        if 'coding_completed' not in existing_columns:
            cursor.execute("""
                ALTER TABLE candidate_auth 
                ADD COLUMN coding_completed BOOLEAN DEFAULT FALSE NOT NULL;
            """)
            print("   ✓ Added coding_completed column")
        
        if 'coding_completed_at' not in existing_columns:
            cursor.execute("""
                ALTER TABLE candidate_auth 
                ADD COLUMN coding_completed_at TIMESTAMP;
            """)
            print("   ✓ Added coding_completed_at column")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Successfully added coding columns to candidate_auth table")
        return True
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"❌ Error migrating candidate_auth table: {str(e)}")
        return False

def create_coding_tables():
    """Create all coding-related tables"""
    print("\n🔧 Creating coding tables...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create coding_problems table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coding_problems (
                id SERIAL PRIMARY KEY,
                problem_id INTEGER UNIQUE NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                difficulty VARCHAR(20) NOT NULL,
                starter_code_python TEXT,
                starter_code_javascript TEXT,
                starter_code_java TEXT,
                starter_code_cpp TEXT,
                test_cases_json JSONB NOT NULL,
                time_limit INTEGER NOT NULL DEFAULT 1000,
                memory_limit INTEGER NOT NULL DEFAULT 128,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create coding_submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coding_submissions (
                id SERIAL PRIMARY KEY,
                candidate_id INTEGER NOT NULL REFERENCES candidate_auth(id),
                problem_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                language VARCHAR(20) NOT NULL,
                status VARCHAR(50) NOT NULL,
                test_results_json JSONB,
                runtime INTEGER,
                memory_usage INTEGER,
                judge0_token VARCHAR(255),
                submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (problem_id) REFERENCES coding_problems(problem_id)
            );
        """)
        
        # Create coding_configuration table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coding_configuration (
                id SERIAL PRIMARY KEY,
                recruiter_id INTEGER UNIQUE NOT NULL REFERENCES recruiter_auth(id),
                problems_count INTEGER NOT NULL DEFAULT 3,
                time_limit_minutes INTEGER NOT NULL DEFAULT 60,
                allowed_languages_json JSONB NOT NULL DEFAULT '["python", "javascript"]'::jsonb,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' 
            AND table_name IN ('coding_problems', 'coding_submissions', 'coding_configuration');
        """)
        
        created_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📊 Tables created: {', '.join(created_tables)}")
        
        # Verify each table
        for table_name in ['coding_problems', 'coding_submissions', 'coding_configuration']:
            if table_name in created_tables:
                print(f"   ✓ {table_name}")
            else:
                print(f"   ⚠ {table_name} not found")
        
        cursor.close()
        conn.close()
        return len(created_tables) == 3
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"❌ Error creating tables: {str(e)}")
        return False

def verify_tables():
    """Verify all tables and their columns"""
    print("\n🔍 Verifying table structure...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check coding_problems table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name='coding_problems' 
            ORDER BY ordinal_position;
        """)
        problems_columns = cursor.fetchall()
        
        print("\n📋 coding_problems columns:")
        for col_name, col_type in problems_columns:
            print(f"   • {col_name} ({col_type})")
        
        # Check coding_submissions table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name='coding_submissions' 
            ORDER BY ordinal_position;
        """)
        submissions_columns = cursor.fetchall()
        
        print("\n📋 coding_submissions columns:")
        for col_name, col_type in submissions_columns:
            print(f"   • {col_name} ({col_type})")
        
        # Check coding_configuration table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name='coding_configuration' 
            ORDER BY ordinal_position;
        """)
        config_columns = cursor.fetchall()
        
        print("\n📋 coding_configuration columns:")
        for col_name, col_type in config_columns:
            print(f"   • {col_name} ({col_type})")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        cursor.close()
        conn.close()
        print(f"❌ Error verifying tables: {str(e)}")
        return False

def insert_sample_data():
    """Insert sample coding problem for testing"""
    print("\n📝 Inserting sample coding problem...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if sample problem already exists
        cursor.execute("SELECT id FROM coding_problems WHERE problem_id = 1;")
        existing = cursor.fetchone()
        
        if existing:
            print("✅ Sample problem already exists")
            cursor.close()
            conn.close()
            return True
        
        # Create sample problem
        test_cases = [
            {
                "input": "[2,7,11,15]\n9",
                "expected_output": "[0,1]",
                "is_hidden": False
            },
            {
                "input": "[3,2,4]\n6",
                "expected_output": "[1,2]",
                "is_hidden": False
            },
            {
                "input": "[3,3]\n6",
                "expected_output": "[0,1]",
                "is_hidden": True
            }
        ]
        
        cursor.execute("""
            INSERT INTO coding_problems (
                problem_id, title, description, difficulty,
                starter_code_python, starter_code_javascript, starter_code_java, starter_code_cpp,
                test_cases_json, time_limit, memory_limit
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, problem_id, title, difficulty;
        """, (
            1,
            "Two Sum",
            """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Constraints:
• 2 <= nums.length <= 104
• -109 <= nums[i] <= 109
• -109 <= target <= 109
• Only one valid answer exists.""",
            "Easy",
            """def twoSum(nums, target):
    # Write your code here
    pass
""",
            """function twoSum(nums, target) {
    // Write your code here
}
""",
            """class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Write your code here
        return new int[]{};
    }
}
""",
            """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Write your code here
    }
};
""",
            Json(test_cases),
            1000,
            128
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        print("✅ Sample problem inserted successfully")
        print(f"   Problem ID: {result[1]}")
        print(f"   Title: {result[2]}")
        print(f"   Difficulty: {result[3]}")
        print(f"   Test cases: {len(test_cases)}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"❌ Error inserting sample data: {str(e)}")
        return False

def main():
    """Main migration function"""
    print("=" * 60)
    print("🚀 CODING ROUND DATABASE MIGRATION")
    print("=" * 60)
    
    print("\n📍 Connecting to database...")
    
    # Step 1: Migrate candidate_auth table
    print("\n" + "=" * 60)
    print("STEP 1: Migrate candidate_auth Table")
    print("=" * 60)
    if not migrate_candidate_auth_table():
        print("\n❌ Migration failed at Step 1")
        return
    
    # Step 2: Create coding tables
    print("\n" + "=" * 60)
    print("STEP 2: Create Coding Tables")
    print("=" * 60)
    if not create_coding_tables():
        print("\n❌ Migration failed at Step 2")
        return
    
    # Step 3: Verify tables
    print("\n" + "=" * 60)
    print("STEP 3: Verify Tables")
    print("=" * 60)
    if not verify_tables():
        print("\n❌ Migration failed at Step 3")
        return
    
    # Step 4: Insert sample data
    print("\n" + "=" * 60)
    print("STEP 4: Insert Sample Data")
    print("=" * 60)
    if not insert_sample_data():
        print("\n⚠️  Warning: Sample data insertion failed (non-critical)")
    
    # Success
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\n📊 Summary:")
    print("   ✓ candidate_auth table updated with coding columns")
    print("   ✓ coding_problems table created")
    print("   ✓ coding_submissions table created")
    print("   ✓ coding_configuration table created")
    print("   ✓ Sample problem inserted")
    print("\n🎉 Your database is ready for the coding round!")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
