from app.extensions import db
from app.models import PsychometricQuestion
from app import create_app

app = create_app()

with app.app_context():
    count = PsychometricQuestion.query.count()
    print(f'✅ Total psychometric questions in database: {count}')
    
    if count == 0:
        print('⚠️  No questions found. Run the load-questions endpoint first.')
    else:
        print(f'✨ Questions are ready for testing!')
