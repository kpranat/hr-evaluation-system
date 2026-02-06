
import sys
import os
# from sqlalchemy import text # This failed, let's try getting it from the app context or just raw string if possible, but execute needs text() usually.
# If sqlalchemy is not finding, maybe it's not in path.
# But flask_sqlalchemy is installed.
try:
    from sqlalchemy import text
except ImportError:
    # Fallback or maybe we need to activate venv
    pass


# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def update_schema():
    app = create_app()
    with app.app_context():
        print("🔄 Updating Schema for Grading Integration...")
        
        # 1. Add grading_json to proctor_sessions if not exists
        try:
            with db.engine.connect() as conn:
                # Check if column exists
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='proctor_sessions' AND column_name='grading_json'"))
                if not result.fetchone():
                    print("➕ Adding grading_json column to proctor_sessions...")
                    conn.execute(text("ALTER TABLE proctor_sessions ADD COLUMN grading_json JSON"))
                    conn.commit()
                    print("✅ Added grading_json column.")
                else:
                    print("ℹ️  grading_json column already exists in proctor_sessions.")
        except Exception as e:
            print(f"❌ Error updating proctor_sessions: {e}")

        # 2. Create CodingAssessmentResult table
        try:
            # We defined it in models.py (I'll need to add it to models.py first actually, or just create it raw SQL here if I want to avoid models.py dependency for this script, but better to update models.py and use migration or create_all)
            # Since we are not using full alembic, let's just create the table via SQL for safety/speed without relying on models.py update taking effect yet
            
            with db.engine.connect() as conn:
                # Check if table exists
                result = conn.execute(text("SELECT to_regclass('public.coding_assessment_results')"))
                if not result.fetchone()[0]:
                     print("➕ Creating coding_assessment_results table...")
                     conn.execute(text("""
                        CREATE TABLE coding_assessment_results (
                            id SERIAL PRIMARY KEY,
                            candidate_id INTEGER NOT NULL UNIQUE REFERENCES candidate_auth(id),
                            score_percentage FLOAT DEFAULT 0.0,
                            grading_json JSON,
                            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
                            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc')
                        )
                     """))
                     conn.commit()
                     print("✅ Created coding_assessment_results table.")
                else:
                    print("ℹ️  coding_assessment_results table already exists.")
                    
        except Exception as e:
            print(f"❌ Error creating coding_assessment_results table: {e}")

if __name__ == "__main__":
    update_schema()
