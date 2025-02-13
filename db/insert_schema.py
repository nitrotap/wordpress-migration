import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Path to schema file
SCHEMA_FILE = "schema.sql"

def execute_schema():
    """Reads and executes the schema.sql file in the Neon PostgreSQL database."""
    try:
        print("Connecting to Neon PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print(f"Applying schema from {SCHEMA_FILE}...")
        with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
            cursor.execute(file.read())

        conn.commit()
        print("Schema applied successfully!")

    except Exception as e:
        print("Error:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    execute_schema()
