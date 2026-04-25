"""
AI Assistant 
Author: Emaan
Description: AI assistant dashboard for different domains (Cybersecurity, IT Operations, Data Science)
             Powered by OpenAI GPT models. Supports chat history, downloading conversations, and clearing chats.
"""

# ====================
# Required Imports 
# ====================
import os
import sys
from pathlib import Path
import streamlit as st
from project.utils import get_assistant_prompt

# Import OpenAI and common API exceptions
from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError

# ====================
# Path setup
# ====================

# Find the main project directory, facilitating local module imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)


# Page configuration
st.set_page_config(page_title="Wave - AI Assistant", layout="wide", page_icon="assets/logo.png")

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


# Define project root and data directory paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent  
DATA_DIR = Path(r"C:\CST1510\CW2_CST1510_M01041173\DATA")


# Create folder for downloaded chats
CHAT_DOWNLOAD_DIR = os.path.join(DATA_DIR, "chat_downloads")
os.makedirs(CHAT_DOWNLOAD_DIR, exist_ok=True)


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

# CSS styling for header
st.markdown(
    f"""
    <div style='font-weight: bold; font-size:28px; text-align:center; 
    color:#0b3d91; border-bottom:3px solid #ff4b4b; margin-top:20px;'>{domain} Chatbot
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("Powered by GPT-4o")

# Display previous messages in expander  (domain specific)
with st.expander("📜 Previous Chat History", expanded=False):
    for message in st.session_state.messages[domain]:
        avatar = USER_ICON if message["role"] == "user" else ASSISTANT_ICON
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


# ---- Sidebar Options
with st.sidebar:
    st.subheader("Chat Controls")

    # Fetch messages from session state
    messages_domain = st.session_state.messages[domain]

    # Display message count
    message_count = len([m for m in messages_domain if m["role"] != "system"])
    st.metric("Messages", message_count)

    # Clear chat button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages[domain] = [{"role": "system", "content": assistant_prompt}]
        st.toast("Chat cleared!", icon="🧹")
        st.rerun()

    # ---- DOWNLOAD CHAT ----
    chat_filename = f"chat.txt"
    chat_filepath = os.path.join(CHAT_DOWNLOAD_DIR, chat_filename)

    # Create the file using file handling
    with open(chat_filepath, "w", encoding="utf-8") as file:
        for m in messages_domain:
            if m["role"] != "system":
                file.write(f"{m['role'].upper()}:\n{m['content']}\n\n")

    # Download button
    with open(chat_filepath, "rb") as file:
        st.sidebar.download_button(
            label="📥 Download Chat",
            data=file,
            file_name=chat_filename,
            mime="text/plain",
            use_container_width=True
        )   

    # Model selection
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=0)

    # Temperature selection
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1,
        help="Higher values make output more random"
    )


# Display chat input box with a dynamic placeholder (domain specific)
prompt = st.chat_input(f"Ask about {domain.lower()}...")

# Display the user's message with user avatar
if prompt:
    with st.chat_message("user", avatar=USER_ICON ):
        st.markdown(prompt)

    # Display user message
    st.session_state.messages[domain].append({"role": "user", "content": prompt})
    
    try:
        # OpenAI Streaming response
        with st.spinner("Thinking..."):
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
    except APIConnectionError as e:
        st.error("Failed to connect to OpenAI API. Check your internet connection.")
        print(e.__cause__)
    except RateLimitError:
        st.error("Rate limit exceeded. Please wait and try again later.")
    except APIStatusError as e:
        st.error(f"OpenAI API returned an error: {e.status_code}")
        st.write(e.response)
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Logout button
if st.button("Log Out"):

    # Update login state
    st.session_state.logged_in = False
    # Display success message
    st.success("Logged out!")
    # Redirect user to Home page
    st.switch_page("Home.py")

