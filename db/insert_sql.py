import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Directory where SQL files are stored
SQL_DIR = "sql_data"


def execute_sql_file(cursor, filename):
    """Reads and executes SQL from a file with error handling."""
    filepath = os.path.join(SQL_DIR, filename)

    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            sql_statements = file.read()
            cursor.execute(sql_statements)
        print(f"✅ Successfully inserted data from {filename}")
        print(len(sql_statements.split(";")) - 1, "SQL statements executed")
        return True

    except psycopg2.IntegrityError as e:
        print(f"❌ IntegrityError while inserting {filename}: {e}")
        cursor.connection.rollback()
    except psycopg2.DataError as e:
        print(f"❌ DataError while inserting {filename}: {e}")
        cursor.connection.rollback()
    except psycopg2.ProgrammingError as e:
        print(f"❌ ProgrammingError while inserting {filename}: {e}")
        cursor.connection.rollback()
    except Exception as e:
        print(f"❌ General Error while inserting {filename}: {e}")
        cursor.connection.rollback()

    return False


def insert_data():
    """Connect to PostgreSQL and insert data into tables with error handling."""
    try:
        print("🚀 Connecting to Neon PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Test connection with a simple query
        cursor.execute("SELECT 1")
        print("✅ Connection test successful")

        # List of SQL files in order of dependency
        sql_files = [
            "authors.sql",
            "posts.sql",
            "pages.sql",
            "categories.sql",
            "tags.sql",
            "seo_data.sql",  # Enable this once posts are verified
            "media.sql",
            "comments.sql",
            "custom_fields.sql",
            "redirects.sql",
        ]

        success_count = 0
        failed_files = []

        print("📥 Inserting data into the database...\n")
        for sql_file in sql_files:
            success = execute_sql_file(cursor, sql_file)
            if success:
                success_count += 1
                conn.commit()  # Commit after each successful file
            else:
                failed_files.append(sql_file)

        print("\n✅ Data insertion complete!")
        print(f"✅ Successfully inserted: {success_count} files")
        if failed_files:
            print(f"❌ Failed to insert: {len(failed_files)} files")
            for failed_file in failed_files:
                print(f"   - {failed_file}")

    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
        print("\n🔌 Database connection closed.")


if __name__ == "__main__":
    insert_data()
