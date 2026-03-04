import mysql.connector
from fastapi import HTTPException

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='task_planner'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise HTTPException(status_code=500, detail="Database connection failed")