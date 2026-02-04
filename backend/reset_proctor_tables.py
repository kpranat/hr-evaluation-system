from app import create_app, db
from app.models import ProctorSession, ProctorEvent, CodePlayback
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Dropping Proctor tables...")
    # Order matters due to foreign keys
    try:
        db.session.execute(text("DROP TABLE IF EXISTS proctor_event CASCADE"))
        db.session.execute(text("DROP TABLE IF EXISTS code_playback CASCADE"))
        db.session.execute(text("DROP TABLE IF EXISTS proctor_session CASCADE"))
        db.session.commit()
    except Exception as e:
        print(f"Error dropping tables: {e}")
        db.session.rollback()

    print("Recreating tables...")
    db.create_all()
    print("Tables reset!")
