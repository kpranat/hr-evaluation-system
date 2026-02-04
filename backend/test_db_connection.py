import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"Testing connection to: {DATABASE_URL[:50]}...")

try:
    # Try to connect
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ PostgreSQL connection successful!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ PostgreSQL version: {version[0][:80]}")
    
    cursor.close()
    conn.close()
    print("✅ Connection closed successfully")
    
except Exception as e:
    print(f"❌ PostgreSQL connection failed!")
    print(f"Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Database server is down or unreachable")
    print("2. Firewall blocking port 6543")
    print("3. Incorrect credentials")
    print("4. Network/VPN required for Supabase access")
