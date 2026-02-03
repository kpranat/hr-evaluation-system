import os
from dotenv import load_dotenv

load_dotenv()  # load .env → environment variables

class Config:
    
    #setup jwt token
    JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
    JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", 10))