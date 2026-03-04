import psycopg2
import os
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment")
            
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as err:
        print(f"Error: {err}")
        raise HTTPException(status_code=500, detail="PostgreSQL connection failed")