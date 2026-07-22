import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("✅ Successfully connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")