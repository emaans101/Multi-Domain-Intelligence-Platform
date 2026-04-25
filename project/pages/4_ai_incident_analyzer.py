"""
AI Analyzer
Author: Emaan
Description: AI Analyzer dashboard for different domains (Cybersecurity, IT Operations, Data Science)
             Powered by OpenAI GPT models. Allows users to select incidents, tickets, or datasets,
             and provides AI-generated analysis including root cause, actions, insights, and recommendations.
             Supports chat-like interaction, session-based message storage, and domain-specific analysis.
"""

# =========================
# Import required modules
# =========================
import os
import sys
import streamlit as st
from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError 


# ====================
# Path setup
# ====================

# Find the main project directory, facilitating local module imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

# ==============================
# Import required local modules
# =============================
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_datasets
from project.utils import get_assistant_prompt


# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) # API key from Streamlit secret

# # --- LOGIN CHECK ---
# # Initialize login state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # --- Validate login ---
# # Redirect if user is not logged in
# if not st.session_state.logged_in:
#     st.error("You must be logged in.")
#     if st.button("Go to Login"):
#         st.switch_page("Home.py")
#     st.stop()

# Page configuration
st.set_page_config(page_title="Wave - AI Analyzer", layout="wide", page_icon="assets/logo.png")

# Display banner
st.image("C:\\CW2\\CW2_CST1510_M01041173_COMPLETE_VERSION-main\\project\\\\assets\\banner4.png", caption="banner image", use_container_width=True)


# Define paths for the database directory and file
PROJECT_DATA_DIR = os.path.join(PROJECT_ROOT, "DATA")
DB_FILE = os.path.join(PROJECT_DATA_DIR, "intelligence_platform.db")

# Establish a connection to the database 
conn = connect_database(DB_FILE)
create_all_tables(conn) # create all required tables


# Fetch data from database tables into global variables
df_incidents = get_all_incidents(conn)
df_datasets = get_all_datasets(conn)
df_tickets = get_all_tickets(conn)

# Domain selection
domain = st.sidebar.selectbox("Select Domain", ["Cybersecurity", "IT Operations", "Data Science"])

# Get assistant prompt
assistant_prompt = get_assistant_prompt(domain)

# Initialise chat messages in session state 
if 'messages' not in st.session_state:
    st.session_state.messages = {
        "Cybersecurity": [{"role": "system", "content": get_assistant_prompt("Cybersecurity")}],
        "IT Operations": [{"role": "system", "content": get_assistant_prompt("IT Operations")}],
        "Data Science": [{"role": "system", "content": get_assistant_prompt("Data Science")}],
    }


# File path for custom avatars 
USER_ICON = "C:\\CW2\\CW2_CST1510_M01041173_COMPLETE_VERSION-main\\project\\assets\\user.png"          
ASSISTANT_ICON = "C:\\CW2\\CW2_CST1510_M01041173_COMPLETE_VERSION-main\\project\\assets\\chatbot.png" 

# CSS styling for Domain header
st.markdown(
    f"""
    <div style='font-weight:bold; font-size:28px; text-align:center;
    color:#0b3d91; border-bottom:3px solid #ff4b4b; margin-top:20px;'>{domain} Analyzer
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("Powered by GPT-4o")

# ------------------- AI ANALYSIS -------------------
def analyze_and_stream(domain_name, incident=None, ticket=None, dataset=None):
    """Generates AI analysis for the selected item using assistant_prompt."""
    
    # --- Create prompt dynamically ---

    # Cybersecurity domain prompt
    if domain_name == "Cybersecurity":
        prompt_text = f"""Analyze this cybersecurity incident:
        Type: {incident['incident_type']}
        Severity: {incident['severity']}
        Description: {incident['description']}
        Status: {incident['status']}

        When analyzing an incident, ALWAYS provide:
        1. Root cause analysis
        2. Immediate actions needed
        3. Long-term prevention measures
        4. Risk assessment (impact + likelihood)

        Tone: Professional, concise, technically accurate
        Format: Bullet points, clear subheadings
        """

    # IT Operations domain prompt
    elif domain_name == "IT Operations":

        prompt_text = f"""Analyze this IT ticket:
        Ticket ID: {ticket['ticket_id']}
        Priority: {ticket['priority']}
        Status: {ticket['status']}
        Category: {ticket['category']}
        Subject: {ticket['subject']}
        Description: {ticket['description']}

        When analyzing a ticket, ALWAYS provide:
        1. Root cause analysis
        2. Immediate actions / troubleshooting steps
        3. Long-term stability & optimization measures
        4. Impact assessment on users/systems

        Tone: Practical, solution-focused
        Format: Clear steps and recommendations
        """
    else:
        # Data Science domain prompt
        prompt_text = f"""Analyze this dataset:

        Name: {dataset['dataset_name']}
        Category: {dataset['category']}
        Source: {dataset['source']}
        Last Updated: {dataset['last_updated']}
        Record Count: {dataset['record_count']}
        File Size (MB): {dataset['file_size_mb']}

        When analyzing a dataset, ALWAYS provide:
        1. Data quality assessment (missing values, outliers, schema issues)
        2. Insights & patterns discovered
        3. Recommended visualizations
        4. Potential ML/statistical techniques that apply

        Tone: Educational, analytical, clear
        Format: Bullet points and explanations when needed
        """
  

    # ---- Sidebar Options
    with st.sidebar:
        st.subheader("Chat Controls")
    
        # Model selection
        model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=0)

        # Temperature selection
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1,
            help="Higher values make output more random"
        )
    
    # Add user prompt to chat history (domain specific)
    st.session_state.messages[domain].append({"role": "user", "content": prompt_text})


    try:
            # OpenAI Streaming response
            completion = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages[domain],
                temperature=temperature,
                stream=True # enable streaming
            )

            # Display assistant streaming response
            with st.chat_message("assistant", avatar=ASSISTANT_ICON):
                container = st.empty() 
                full_reply = "" 

                # Process each chunk as it arrives
                for chunk in completion:
                    delta = chunk.choices[0].delta
                    if delta.content: 
                        full_reply += delta.content 
                        container.markdown(full_reply + "▌") # add cursor affect

                # Remove cursor and show final response
                container.markdown(full_reply) 

                # Save complete assistant message (domain specific)
                st.session_state.messages[domain].append({"role": "assistant", "content": full_reply})

    # Error Handling with OpenAI API
    except APIConnectionError:
        st.error("Failed to connect to OpenAI API.")
    except RateLimitError:
        st.error("Rate limit exceeded. Try again later.")
    except APIStatusError as e:
        st.error(f"OpenAI API returned an error: {e.status_code}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# ===== Domain-Specific Analyzer =====

# Initialize selected domain placeholder
selected_item = None

# === Cybersecurity domain Analyzer ===
if domain == "Cybersecurity":

    # Convert incidents to a list
    incident_list = df_incidents .to_dict(orient="records")

    # User select incidents from dropdown menu
    selected_idx = st.selectbox(
        "Select incident to analyze:",
        range(len(incident_list)),
        format_func=lambda i: f"{incident_list[i]['id']}: {incident_list[i]['incident_type']} - {incident_list[i]['severity']}",
        key="incident_select"
    )

    # Display details of Cybersecurity 
    selected_item = incident_list[selected_idx]
    st.subheader("📋 Incident Details")
    st.write(selected_item)

    # Provide AI analysis for Cybersecurity
    if st.button("🤖 Analyze Incident", key="analyze_incident"):
        with st.spinner("AI analyzing incident..."):
            analyze_and_stream("Cybersecurity", incident=selected_item)

# === IT Operations domain Analyzer ===
elif domain == "IT Operations":

    # Convert tickets to a list
    ticket_list = df_tickets.to_dict(orient="records")

    # User select tickets from dropdown menu
    selected_idx = st.selectbox(
        "Select ticket to analyze:",
        range(len(ticket_list)),
        format_func=lambda i: f"{ticket_list[i]['ticket_id']}: {ticket_list[i]['subject']} - {ticket_list[i]['priority']}",
        key="ticket_select"
    )

    # Display details of IT Operations
    selected_item = ticket_list[selected_idx]
    st.subheader("📋 Ticket Details")
    st.write(selected_item)

    # Provide AI analysis for IT Operations
    if st.button("🤖 Analyze Ticket", key="analyze_ticket"):
        with st.spinner("AI analyzing ticket..."):
            analyze_and_stream("IT Operations", ticket=selected_item)

# === Data Science domain Analyzer ===
elif domain == "Data Science":

    # Convert Data Science to a list
    dataset_list = df_datasets.to_dict(orient="records")

    # Display details of Data Science
    selected_idx = st.selectbox(
        "Select dataset to analyze:",
        range(len(dataset_list)),
        format_func=lambda i: f"{dataset_list[i]['dataset_name']} - {dataset_list[i]['category']}",
        key="dataset_select"
    )

    # Display details of Data Science
    selected_item = dataset_list[selected_idx]
    st.subheader("📋 Dataset Details")
    st.write(selected_item)

    # Provide AI analysis for Data Science
    if st.button("🤖 Analyze Dataset", key="analyze_dataset"):
        with st.spinner("AI analyzing dataset..."):
            analyze_and_stream("Data Science", dataset=selected_item)

# Display previous messages in expander  (domain specific)
with st.expander("📜 Previous Chat History", expanded=False):
    for message in st.session_state.messages[domain]:
        avatar = USER_ICON if message["role"] == "user" else ASSISTANT_ICON
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Logout button
if st.button("Log Out"):

    # Update login state
    st.session_state.logged_in = False
    # Display success message
    st.success("Logged out!")
    # Redirect user to Home page
    st.switch_page("Home.py")
