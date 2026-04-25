# ====================
# Required Imports 
# ====================
import streamlit as st
import os
import sys

# ====================
# Path setup
# ====================

# Find the main project directory, facilitating local module imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

# ==============================
# Import required local modules
# ==============================
from app.data.db import connect_database, load_all_csv_data
from app.data.schema import create_all_tables

# Utility functions
from project.utils import view_records, add_new_record, update_delete_record

# Define paths for the database directory and file
PROJECT_DATA_DIR = os.path.join(PROJECT_ROOT, "DATA")
DB_FILE = os.path.join(PROJECT_DATA_DIR, "intelligence_platform.db")

# Establish a connection to the database 
conn = connect_database(DB_FILE)
create_all_tables(conn) # create all required tables

# Load CSV files into their tables
load_all_csv_data(conn, os.path.join(PROJECT_DATA_DIR, "cyber_incidents.csv"), "cyber_incidents")
load_all_csv_data(conn, os.path.join(PROJECT_DATA_DIR, "it_tickets.csv"), "it_tickets")
load_all_csv_data(conn, os.path.join(PROJECT_DATA_DIR, "datasets_metadata.csv"), "datasets_metadata")


# --- LOGIN CHECK ---
# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

 # --- Validate login ---
# Redirect if user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Page configuration 
st.set_page_config(page_title="Wave - Dashboard", layout="wide", page_icon="assets/logo.png")

# Display banner
st.image("C:\\CW2\\CW2_CST1510_M01041173_COMPLETE_VERSION-main\\project\\\\assets\\banner2.png", caption = "banner image", use_container_width=True)

# Sidebar for selecting domain and options
domain_selection = st.sidebar.selectbox("Select Domain", ["Cybersecurity", "IT Operations", "Data Science"])

# Define options list
available_options =  ["📄 View Records", "➕ Add New Record", "✏ Update / Delete"]

# Display options list on sidebar
option_selection = st.sidebar.multiselect(
    "Select Options", available_options, default="📄 View Records"
    )

# Select database table based on sidebar domain choice
domain_options = {
    "Cybersecurity": "cyber_incidents",
    "IT Operations": "it_tickets",
    "Data Science": "datasets_metadata"
}

# Fetch database table based on user domain selection
selected_table = domain_options[domain_selection]

# ================================================
# Call CRUD functions based on user chosen 
# ================================================

# Display all records from selected database table
if "📄 View Records" in option_selection:
    view_records(conn, selected_table)

# Add new record to the selected database table
if "➕ Add New Record" in option_selection:
    add_new_record(conn, selected_table)

# Manuplate the selected database table
if "✏ Update / Delete" in option_selection:
    update_delete_record(conn, selected_table)
    st.stop()

# --- LOGOUT ---
st.divider()

# Logout button
if st.button("Log Out"):

    # Update login state
    st.session_state.logged_in = False
    # Display message
    st.success("Logged out!")
    # Redirect user to Home page
    st.switch_page("Home.py")

