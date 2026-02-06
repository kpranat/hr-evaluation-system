"""Migration script to add exam tracking and suspension fields to database"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import db
from app.models import ProctorSession, IntegrityLog
from sqlalchemy import text
from datetime import datetime

def migrate_database():
    """Add new columns to ProctorSession and create IntegrityLog table"""
    print("Starting database migration...")
    
    try:
        with db.engine.connect() as conn:
            # Add new columns to proctor_sessions table
            print("\n1. Adding new columns to proctor_sessions table...")
            
            columns_to_add = [
                ("last_activity", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                ("current_question_index", "INTEGER DEFAULT 0"),
                ("is_suspended", "BOOLEAN DEFAULT FALSE"),
                ("suspension_reason", "VARCHAR(255)"),
                ("resume_allowed", "BOOLEAN DEFAULT FALSE")
            ]
            
            for column_name, column_def in columns_to_add:
                try:
                    query = f'ALTER TABLE proctor_sessions ADD COLUMN IF NOT EXISTS {column_name} {column_def}'
                    conn.execute(text(query))
                    conn.commit()
                    print(f"   ✓ Added column: {column_name}")
                except Exception as e:
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"   ⊙ Column {column_name} already exists")
                        conn.rollback()
                    else:
                        print(f"   ✗ Error adding {column_name}: {e}")
                        conn.rollback()
            
            # Update existing records to have last_activity set to their start_time
            print("\n2. Updating existing records with default values...")
            try:
                update_query = text("""
                    UPDATE proctor_sessions 
                    SET last_activity = COALESCE(last_activity, start_time, CURRENT_TIMESTAMP)
                    WHERE last_activity IS NULL
                """)
                result = conn.execute(update_query)
                conn.commit()
                print(f"   ✓ Updated {result.rowcount} existing records")
            except Exception as e:
                print(f"   ⊙ Update info: {e}")
            
            # Create integrity_logs table
            print("\n3. Creating integrity_logs table...")
            try:
                create_table_query = text("""
                    CREATE TABLE IF NOT EXISTS integrity_logs (
                        id SERIAL PRIMARY KEY,
                        session_id INTEGER NOT NULL,
                        event VARCHAR(100) NOT NULL,
                        severity VARCHAR(20) NOT NULL,
                        details TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        FOREIGN KEY (session_id) REFERENCES proctor_sessions (id)
                    )
                """)
                conn.execute(create_table_query)
                conn.commit()
                print("   ✓ Created integrity_logs table")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("   ⊙ Table integrity_logs already exists")
                    conn.rollback()
                else:
                    print(f"   ✗ Error creating table: {e}")
                    conn.rollback()
            
            print("\n✅ Migration completed successfully!")
            print("\nNew features available:")
            print("  • Heartbeat tracking via last_activity")
            print("  • Exam suspension and resume capability")
            print("  • Structured integrity logging")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    from run import app
    
    with app.app_context():
        success = migrate_database()
        
        if success:
            # Verify tables exist
            print("\n" + "="*60)
            print("Verifying database schema...")
            try:
                with db.engine.connect() as conn:
                    # Check proctor_sessions columns
                    result = conn.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'proctor_sessions'
                    """))
                    columns = [row[0] for row in result]
                    
                    required_columns = ['last_activity', 'current_question_index', 
                                      'is_suspended', 'suspension_reason', 'resume_allowed']
                    
                    print("\nProctorSession columns:")
                    for col in required_columns:
                        status = "✓" if col in columns else "✗"
                        print(f"  {status} {col}")
                    
                    # Check integrity_logs table
                    result = conn.execute(text("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_name = 'integrity_logs'
                    """))
                    table_exists = result.fetchone() is not None
                    
                    print("\nIntegrityLog table:")
                    print(f"  {'✓' if table_exists else '✗'} integrity_logs")
                    
                    if table_exists:
                        result = conn.execute(text("SELECT COUNT(*) FROM integrity_logs"))
                        count = result.fetchone()[0]
                        print(f"     Current records: {count}")
                
                print("\n✅ Verification complete!")
            except Exception as e:
                print(f"\n⚠ Verification warning: {e}")
        else:
            sys.exit(1)
