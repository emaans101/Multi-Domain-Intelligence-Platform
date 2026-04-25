"""
Name: Emaan Fatima
MISI: M01041173
Course: CST1510 - Programming for Data Communication and Networks
File: utils.py
Description: This file contains utility/helper functions used across the application
             
"""

# ====================
# Required Imports 
# ====================
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

# ====================
# Path setup
# ====================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

# ==============================
# Import required local modules
# ==============================
from app.data.db import connect_database
from app.data.schema import create_all_tables

# Cybersecurity
from app.data.incidents import (
     insert_incident, get_all_incidents,
    update_incident_status, delete_incident,
)

# IT Operations
from app.data.tickets import (
    insert_ticket, get_all_tickets,
    update_ticket, delete_ticket,
)

# Data Science
from app.data.datasets import (
     insert_dataset, update_dataset, get_all_datasets,
     delete_dataset
)

# Define paths for the database directory and file
DATA_DIR = os.path.join(ROOT_DIR, "DATA")
DB_FILE = os.path.join(DATA_DIR, "intelligence_platform.db")

# Establish a connection to the database
conn = connect_database(DB_FILE)
create_all_tables(conn) # create all required tables


# View Records function
def view_records(conn, table_name):
        
        # Custom styling with CSS
        st.markdown(
"""    
        <style>
        .table-header {font: bold 28px "Segoe UI", Roboto, sans-serif; color:#0b3d91; border-bottom:3px solid #ff4b4b; margin-bottom:10px;}
        table {border-collapse:collapse; width:100%;}
        th {background:#0b3d91; color:#fff; padding:8px; text-align:left;}
        td {padding:6px; border-bottom:1px solid #ddd;}
        tr:hover {background:#f1f1f1;}
        </style>
        """,
        unsafe_allow_html=True
    )
        
        # Fetch data based on the table name
        if table_name == "cyber_incidents":
            df = get_all_incidents(conn)

            # Display Header
            st.markdown('<div class="table-header">🔒 Cyber Incidents</div>', unsafe_allow_html=True)

        elif table_name == "it_tickets":
            df = get_all_tickets(conn)

            # Display Header
            st.markdown('<div class="table-header">💻 IT Tickets</div>', unsafe_allow_html=True)

        elif table_name == "datasets_metadata":
            df = get_all_datasets(conn)

            # Display Header
            st.markdown('<div class="table-header">📊 Data Science Datasets</div>', unsafe_allow_html=True)

        # Display the dataframe in Streamlit
        st.dataframe(df, use_container_width=True)


# Function to Add New Record 
def add_new_record(conn, table_name):

    # Add new record in Cybersecurity 
    if table_name == "cyber_incidents":

        # Display Header
        st.subheader("Add New Cybersecurity Incident")

        with st.form("new_incident"):

            # Avalible fields for the new incident
            date = st.date_input("Date")
            incident_type = st.selectbox("Incident Type", ["Phishing", "Malware", "DDoS", "Ransomware"])
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "Investigating", "Resolved", "Closed"])
            description = st.text_area("Description")
            reported_by = st.text_input("Reported by")

            # Submit button for the form
            submitted = st.form_submit_button("Add Incident")

            if submitted:
                # Add new incident into the database
                insert_incident(conn, str(date), incident_type, severity, status, description, reported_by)
                st.success("✓ Incident added successfully!")
                st.rerun()

    # Add new record in IT Ticket
    elif table_name == "it_tickets":
        
        # Display Header
        st.subheader("Add New IT Ticket")

        # Avalible fields for the new ticket
        with st.form("add_ticket"):
            ticket_id = st.text_input("Ticket ID")
            priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
            category = st.text_input("Category")
            subject = st.text_input("Subject")
            description = st.text_area("Description")
            created_date = st.date_input("Created Date")
            resolved_date = st.date_input("Resolved Date", value=None)
            assigned_to = st.text_input("Assigned To")

            # Submit button for the form
            submitted = st.form_submit_button("Add Ticket")

            if submitted:
                # Add new ticket into the database
                insert_ticket(conn, ticket_id, priority, status, category, subject, description,
                              str(created_date), str(resolved_date), assigned_to)
                st.success("✓ Ticket added successfully!")
                st.rerun()

    # Add new record in Data Science 
    elif table_name == "datasets_metadata":

        # Display Header
        st.subheader("Add New Dataset Metadata")

        # Avalible fields for the new dataset
        with st.form("add_dataset_form"):
            dataset_name = st.text_input("Dataset Name")
            category = st.selectbox("Category", ["Threat Intelligence", "Network Logs", "User Data", "Other"])
            source = st.text_input("Source / Origin")
            last_updated = st.date_input("Last Updated")
            record_count = st.number_input("Record Count", min_value=0, step=1)
            file_size_mb = st.number_input("File Size (MB)", min_value=0.0, step=0.01)

            # Submit button for the form
            submitted = st.form_submit_button("Add Dataset")

            if submitted:
                try:
                    # Add new dataset into the database
                    insert_dataset(conn, dataset_name, category, source, str(last_updated), record_count, file_size_mb)
                    st.success(f"✓ Dataset '{dataset_name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to add dataset: {e}")

# Update & Delete exisiting Record 
def update_delete_record(conn, table_name):

    # Define tables and their corresponding functions and primary keys
    domain_options = {
    "cyber_incidents": (get_all_incidents, "id"),
    "it_tickets": (get_all_tickets, "ticket_id"),
    "datasets_metadata": (get_all_datasets, "dataset_name")
    }

    # Error Handling
    if table_name not in domain_options:
        st.info("Table not found")
        return

    # Exract function and key
    df_function, domain_key = domain_options[table_name]
    df = df_function(conn)

    # Convert the dataframe to a list of dictionaries
    convert_record_list = df.to_dict("records")

    # Extract the domain ids
    domain_ids = [r[domain_key] for r in convert_record_list]

    # User select a record
    user_selection = st.selectbox(f"Select record ({domain_key})", domain_ids)
    index = domain_ids.index(user_selection)

    # Retrieve the entire record as a dictionary
    record = convert_record_list[index]

    # Update / Delete Form 
    with st.form("update_delete_form"):

        # Initialize dictionary
        user_inputs = {}

        # Provide selection options
        selected_action = st.radio("Action", ["Update", "Delete"])

         # Cyber Incidents Form
        if table_name == "cyber_incidents":
            st.subheader("Edit Cyber Incident")

            # Loop over each field 
            for field, value in record.items():
                if field == domain_key:
                    user_inputs[field] = st.text_input(field, value, disabled=True)
                
                # Only 'status' is editable in Cyber Incident
                elif field == "status":  
                    options = ["Open", "In Progress", "Closed", "Resolved", "Investigating"]
                    current_status = value 
                    user_inputs[field] = st.selectbox("Status", options, index=options.index(current_status))
                else:

                    # Display only the other fields
                    st.text_input(field, value, disabled=True)

        # Datasets Metadata Form
        elif table_name == "datasets_metadata":
            st.subheader("Edit Dataset")

            # Loop over each field 
            for field, value in record.items():
                if field == domain_key:
                    user_inputs[field] = st.text_input(field, value, disabled=True)

                # Only 'record_count' is editable in  Datasets Metadata
                elif field == "record_count": 
                    user_inputs[field] = st.number_input("Record Count", value=int(value))
                else:  

                    # Display only the other fields
                    st.text_input(field, value, disabled=True)

        # IT Tickets Form
        elif table_name == "it_tickets":
            st.subheader("Edit Ticket")

            # Loop over each field 
            for field, value in record.items():
                if field == domain_key:
                    user_inputs[field] = st.text_input(field, value, disabled=True)
                
                # Only 'status' is editable for IT tickets
                elif field == "status":  
                    status_options = ["Open", "In Progress", "Closed", "Resolved", "Investigating"]
                    current_status = value
                    user_inputs[field] = st.selectbox("Status", status_options, index=status_options.index(current_status))
                else:  
                    # Display only the other fields
                    st.text_input(field, value, disabled=True)

         # Submit button
        submit = st.form_submit_button("Submit")

    # Perform Update or Delete based on user choice
    if submit:

        # Call update function
        if selected_action == "Update":

            # Perform on cyber_incidents
            if table_name == "cyber_incidents":
                update_incident_status(conn, user_selection, user_inputs.get("status"))
                st.success(f"Incident '{user_selection}' updated successfully!")

            # Perform on it_tickets
            elif table_name == "it_tickets":
                update_ticket(conn, user_selection, user_inputs.get("status"))
                st.success(f"Ticket '{user_selection}' updated successfully!")

            # Perform on datasets_metadata
            elif table_name == "datasets_metadata":
                update_dataset(conn, user_selection, user_inputs.get("record_count"))
                st.success(f"Dataset '{user_selection}' updated successfully!")

        # Call delete function
        elif selected_action == "Delete":
            
            # Perform on cyber_incidents
            if table_name == "cyber_incidents":
                delete_incident(conn, user_selection)
            
            # Perform on it_tickets
            elif table_name == "it_tickets":
                delete_ticket(conn, user_selection)
            
                # Perform on datasets_metadata
            elif table_name == "datasets_metadata":
                delete_dataset(conn, user_selection)
            st.success("Record deleted!")

        st.rerun()

# -------------------- Assistant Prompt Function --------------------
def get_assistant_prompt(domain: str) -> str:
    """Return a domain-specific assistant prompt for Chat GPT."""
    
    # Cybersecurity Domain prompt
    if domain == "Cybersecurity":
        return """
        You are a cybersecurity expert AI assistant.
        - Analyze incidents and threats
        - Perform incident triage and threat intelligence lookup
        - Provide technical guidance using standard references (MITRE ATT&CK, CVE)
        - Explain attack vectors and mitigations, and security best practices
        - Prioritize actionable recommendations
        Tone: Professional, technical
        Format: Clear, structured responses
    """

    # IT Operations Domain prompt
    elif domain == "IT Operations":
        return """
        You are an IT operations specialist AI assistant.
        - Triage and prioritize support tickets
        - Troubleshoot systems, networking, cloud, and databases
        - Provide step-by-step guidance and practical solutions
        - Recommend system improvements and optimizations
        - Explain technical issues clearly
        - Share infrastructure best practices following ITIL principles
        Tone: Professional, technical
        Format: Clear, structured responses
        """

    # Data Science Domain prompt
    elif domain == "Data Science":
        return """
        You are a Data Science expert AI assistant.
        - Suggest analysis methods and statistical tests
        - Recommend visualizations and explain their use
        - Provide data cleaning and preprocessing strategies
        - Explain ML models and statistical methods
        - Provide Python examples using pandas, sklearn, or other relevant libraries
        - Analyze datasets and provide actionable insights
        Tone: Professional, technical
        Format: Clear, structured responses
    """
