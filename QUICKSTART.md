# Quick Start - Local Development

## Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL
- Supabase account
- Groq API key

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Configure your `.env` file with your database credentials

6. Run the backend:
```bash
python run.py
```

Backend will run on `http://localhost:5000`

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Configure your `.env` file:
```env
VITE_API_URL=http://localhost:5000
```

5. Run the frontend:
```bash
npm run dev
```

Frontend will run on `http://localhost:8080`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.
