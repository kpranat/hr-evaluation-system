"""
Migration script to add partial scoring columns to coding_submissions table
"""

from app import create_app
from app.extensions import db

def migrate_coding_submissions():
    """Add passed_test_cases, total_test_cases, and score_percentage columns"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Starting migration for coding_submissions table...")
            
            # Add the new columns
            with db.engine.connect() as conn:
                # Add passed_test_cases column
                try:
                    conn.execute(db.text("""
                        ALTER TABLE coding_submissions 
                        ADD COLUMN passed_test_cases INTEGER NOT NULL DEFAULT 0
                    """))
                    conn.commit()
                    print("✅ Added passed_test_cases column")
                except Exception as e:
                    if "already exists" in str(e):
                        print("⚠️  passed_test_cases column already exists")
                    else:
                        raise
                
                # Add total_test_cases column
                try:
                    conn.execute(db.text("""
                        ALTER TABLE coding_submissions 
                        ADD COLUMN total_test_cases INTEGER NOT NULL DEFAULT 0
                    """))
                    conn.commit()
                    print("✅ Added total_test_cases column")
                except Exception as e:
                    if "already exists" in str(e):
                        print("⚠️  total_test_cases column already exists")
                    else:
                        raise
                
                # Add score_percentage column
                try:
                    conn.execute(db.text("""
                        ALTER TABLE coding_submissions 
                        ADD COLUMN score_percentage DOUBLE PRECISION NOT NULL DEFAULT 0.0
                    """))
                    conn.commit()
                    print("✅ Added score_percentage column")
                except Exception as e:
                    if "already exists" in str(e):
                        print("⚠️  score_percentage column already exists")
                    else:
                        raise
            
            print("\n✅ Migration completed successfully!")
            print("📊 New columns added:")
            print("   - passed_test_cases (INTEGER, default 0)")
            print("   - total_test_cases (INTEGER, default 0)")
            print("   - score_percentage (DOUBLE PRECISION, default 0.0)")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_coding_submissions()
