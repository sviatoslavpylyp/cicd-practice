import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class UserDAO:
    def __init__(self):
        # Construct the connection URL from environment variables
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

        # Use the connection URL to connect to the database
        self.conn = psycopg2.connect(db_url)

    def _initialize_schema(self):
        """Create schema and tables if they do not already exist."""
        with self.conn.cursor() as cursor:
            # Create schema if it doesn't exist
            cursor.execute("CREATE SCHEMA IF NOT EXISTS app_schema;")

            # Create users table within the schema
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_schema.users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
            """)
            self.conn.commit()

    def create_user(self, name, email):
        """Inserts a new user into the users table."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s);",
                    (name, email)
                )
                self.conn.commit()
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()  # Rollback if unique violation error
            print(f"User with email {email} already exists.")
        except psycopg2.Error as e:
            self.conn.rollback()  # Rollback any other error
            print(f"Error occurred: {e}")
            raise e

    def get_all_users(self):
        """Fetches all users from the users table."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            return users

    def __del__(self):
        """Close the database connection when DAO is deleted."""
        self.conn.close()
