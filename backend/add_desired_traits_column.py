"""
Migration Script: Add desired_traits column to psychometric_test_config table

This script adds the desired_traits column to store which personality traits
recruiters are looking for in candidates.

Usage:
    python add_desired_traits_column.py
"""

from app import create_app
from app.extensions import db
from sqlalchemy import text, inspect

def add_desired_traits_column():
    """Add desired_traits column if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ADDING DESIRED_TRAITS COLUMN TO PSYCHOMETRIC_TEST_CONFIG")
        print("=" * 60)
        
        try:
            inspector = inspect(db.engine)
            
            # Check if table exists
            if 'psychometric_test_config' not in inspector.get_table_names():
                print("❌ Table 'psychometric_test_config' does not exist!")
                print("   Please run the psychometric test setup first.")
                return False
            
            # Check if column already exists
            columns = [col['name'] for col in inspector.get_columns('psychometric_test_config')]
            
            if 'desired_traits' in columns:
                print("✓ Column 'desired_traits' already exists")
                return True
            
            # Add the column
            print("\n[Step 1/2] Adding 'desired_traits' column...")
            db.session.execute(text("""
                ALTER TABLE psychometric_test_config 
                ADD COLUMN desired_traits TEXT
            """))
            db.session.commit()
            print("✓ Column added successfully")
            
            # Verify the column was added
            print("\n[Step 2/2] Verifying column...")
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('psychometric_test_config')]
            
            if 'desired_traits' in columns:
                print("✓ Column verified successfully")
                print("\n" + "=" * 60)
                print("✅ MIGRATION COMPLETE")
                print("=" * 60)
                print("\nThe desired_traits column has been added to store")
                print("personality traits that recruiters are looking for.")
                return True
            else:
                print("❌ Column verification failed")
                return False
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = add_desired_traits_column()
    exit(0 if success else 1)
