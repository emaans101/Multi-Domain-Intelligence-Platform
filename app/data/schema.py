"""
schema.py - Define functions to create database tables

Tables included:
    • users
    • cyber_incidents
    • datasets_metadata
    • it_tickets
    • chat_history
"""

# -----------------
# Import modules
# -----------------
import sqlite3 # required for error handling

# --------------------------------------
# Helper function to create a table
# --------------------------------------
def create_table(conn, sql, table_name):
    """
    Create a table using the provided SQL statement.
    Args:
        conn: Database connection object
        sql: SQL statement to create the table
        table_name: Name of the table to be created
    """
    try:
        # Execute the SQL statement
        with conn:
            # Execute the SQL command
            conn.execute(sql)

        # Display success message
        print(f"✅ '{table_name}' table created successfully!")

    # Handle exceptions during table creation
    except sqlite3.Error as e:
        print(f"❌ Error creating '{table_name}' table: {e}")

# --------------------------------------
# Function to create 'users' table
# --------------------------------------

def create_users_table(conn):
    """
    Create the users table if it doesn't exist.

    Args:
        conn: Database connection object
    """

    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    # Call the helper function to create the table
    create_table(conn, create_table_sql, 'users')


# --------------------------------------------
# Function to create 'cyber_incidents' table
# --------------------------------------------

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - date: TEXT (format: YYYY-MM-DD)
    - incident_type: TEXT (e.g., 'Phishing', 'Malware', 'DDoS')
    - severity: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'Investigating', 'Resolved', 'Closed')
    - description: TEXT
    - reported_by: TEXT (username of reporter)
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    
    # SQL statement to create 'cyber_incidents' table
    # Write CREATE TABLE IF NOT EXISTS SQL statement
    create_table_sql = """
             CREATE TABLE IF NOT EXISTS cyber_incidents (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             date TEXT,
             incident_type TEXT,
             severity TEXT,
             status TEXT,
             description TEXT,
             reported_by TEXT,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    # Call the helper function to create the table
    create_table(conn, create_table_sql, 'cyber_incidents')

   
# ------------------------------------------------------------------------
# Function to create 'datasets_metadata' table
# -----------------------------------------------------------------------

def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - dataset_name: TEXT NOT NULL
    - category: TEXT (e.g., 'Threat Intelligence', 'Network Logs')
    - source: TEXT (origin of the dataset)
    - last_updated: TEXT (format: YYYY-MM-DD)
    - record_count: INTEGER
    - file_size_mb: REAL
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """

    # SQL statement to create 'datasets_metadata' table
    create_table_sql = """
             CREATE TABLE IF NOT EXISTS datasets_metadata (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             dataset_name TEXT NOT NULL,
             category TEXT,
             source TEXT,
             last_updated TEXT,
             record_count INTEGER,
             file_size_mb REAL,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   
    )
    """
    # Call the helper function to create the table
    create_table(conn, create_table_sql, 'datasets_metadata')   
    

# ------------------------------------
# Function to create it_tickets table
# ------------------------------------
def create_it_tickets_table(conn):
    """
    Create the it_tickets table if it doesn't exist.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - ticket_id: TEXT UNIQUE NOT NULL
    - priority: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'In Progress', 'Resolved', 'Closed')
    - category: TEXT (e.g., 'Hardware', 'Software', 'Network')
    - subject: TEXT NOT NULL
    - description: TEXT
    - created_date: TEXT (format: YYYY-MM-DD)
    - resolved_date: TEXT
    - assigned_to: TEXT
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """

    # SQL statement to create 'it_tickets' table
    create_table_sql = """
                CREATE TABLE IF NOT EXISTS it_tickets (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                priority TEXT,
                status TEXT,
                category TEXT,
                subject TEXT NOT NULL,
                description TEXT,
                created_date TEXT,
                resolved_date TEXT,
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """                   
    # Call the helper function to create the table
    create_table(conn, create_table_sql, 'it_tickets')


# --------------------
# Create all tables 
# --------------------

def create_all_tables(conn):
    """
    Create all four tables in the database.

    Args:
        conn: Database connection object
    """

    # Call functions of every table
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

# --- End of schema.py ---
