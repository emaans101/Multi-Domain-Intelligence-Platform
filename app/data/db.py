"""
db.py - Utility functions for database operations.

Provides helper functions for:
    • Connecting to the SQLite database
    • Loading CSV files into tables 
"""

# -------------------------------
# Import required libraries
# -------------------------------
import sqlite3
from pathlib import Path
import pandas as pd

# -------------------------------
# Define paths
# -------------------------------
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# ------------------------------------
# Connect to the SQLite database
# ------------------------------------
def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Create the database file if it doesn't exist.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        sqlite3.Connection: Database connection object
    """

    # Handle database connection errors using try-except
    try:
        return sqlite3.connect(str(db_path))
    
    # Handle SQLite errors during database connection
    except sqlite3.Error as e:
         print(f"⚠️ Error occurred! database not connected {e}")
         return None
    
# ------------------------------------
# Load CSV data into a table
# ------------------------------------
def load_all_csv_data(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    
    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table
        
    Returns:
        int: Number of rows loaded
    """
    try:
        # Check if CSV file exists
        csv_path = Path(csv_path)
        if not csv_path.exists():
            print(f"'{csv_path}' not found")
            return 0
        
        # ------------------------------------
        # Read CSV using pandas
        # ------------------------------------
        df = pd.read_csv(csv_path)

        # Validate if CSV is empty 
        if df.empty:
            print(f"⚠️ CSV '{csv_path}' is empty. No rows loaded.")
            return 0

        # If 'id' column exists, drop it (to avoid conflicts with AUTOINCREMENT)
        if "id" in df.columns:
            df = df.drop(columns=["id"])

        # ------------------------------------
        # Insert data into table
        # ------------------------------------
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        conn.commit()

        # ------------------------------------
        # Print success message and return count
        # ------------------------------------
        row_count = len(df)
        print(f"✅ Successfully loaded '{table_name}' ({row_count} rows)")
        return row_count

    # Handle SQLite errors during database connection
    except Exception as e:
        print(f"⚠️ Error occurred '{table_name}' from '{csv_path}': {e}")
        return 0
    
