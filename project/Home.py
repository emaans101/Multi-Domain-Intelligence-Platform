# ====================
# Required Imports 
# ====================
import streamlit as st

# Import local module for authentication
from authentication import (
    register_user,
    login_user,
    user_exists,
    validate_username,
    validate_password,
    check_password_strength,
    create_session,
    USER_DATA_FILE,
)

# Page configuration 
st.set_page_config(page_title="Wave - Homepage", layout="wide", page_icon="assets/logo.png")

# Display banner
st.image("C:\\CW2\\CW2_CST1510_M01041173_COMPLETE_VERSION-main\\project\\\\assets\\banner.png", caption = "banner image", use_container_width =True)

# Display custom header & image
st.markdown(
    """
    <h1 style='display:flex; align-items:center; gap:10px;'>
        <img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png" width="35"/>
         Welcome to Wave
    </h1>
    """,
    unsafe_allow_html=True
)

# Display caption
st.caption("Register / Login")

# ---------- Initialize Session state ----------

# Validate if user logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Store username after login
if "username" not in st.session_state:
    st.session_state.username = ""

# Assign default tab to Login
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Login"


# -----Redirect user if already logged in -----
if st.session_state.logged_in:
    
    # Display messgae user already logged in
    st.success(f"Already logged in as **{st.session_state.username}**.")

    # Display button to redirect 
    if st.button("🔗 Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# Provide login/register tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    # Placeholder variables to hold the user's username and password
    login_username = st.text_input("Username", key="login_username") 
    login_password = st.text_input("Password", type="password", key="login_password")

    # ---- Login Button ----
    if st.button("Log In", type="primary"):

        # Check if fields are empty before calling login_user()
        if not login_username:
            st.error("❌ Username must not be empty.")

        elif not login_password:
            st.error("❌ Password must not be empty.")

        # Validate if user already exists
        elif not USER_DATA_FILE.exists() or not user_exists(login_username):
            st.error(f"❌ Username '{login_username}' not found. Please register first.")

        # Login User when credential valid
        else:
            login_result = login_user(login_username, login_password)

            # Update session state after user login
            if login_result is True:
                st.session_state.logged_in = True
                st.session_state.username = login_username

                # Create session & display message
                st.success(f"🎉 Welcome back, {login_username}!")
                create_session(login_username)
                st.balloons()
            else:
                # Display error message
                st.error(login_result)

    # ---- Show dashboard button if logged in ----
    if st.session_state.logged_in:
        if st.button("🔗 Dashboard"):
            st.switch_page("pages/1_Dashboard.py")


# ----- REGISTER TAB -----
with tab_register:
        st.subheader("Register")
        
        # Ask for username & password
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

        # Role selection
        user_role_options = ["user", "admin", "analyst"]
        selected_role = st.selectbox("Select your role", user_role_options)

        if st.button("Create account"):

            # Validation username using function
            valid_user, msg_user = validate_username(new_username)
            if not valid_user:
                st.error(msg_user)

            # Check if username alread exists 
            elif user_exists(new_username):
                st.error("Username already exists.")

            else:
                # Validate user passowrd
                valid_pwd, display_msg = validate_password(new_password, new_username)
                if not valid_pwd:
                    st.error(display_msg)

                else:
                    # Check password strength 
                    strength_check, strength_msg = check_password_strength(new_password)

                    # Display strength to progress bar
                    strength_bar = {"Weak": 0.25, "Moderate": 0.66, "Strong": 1.0}
                    st.progress(strength_bar.get(strength_msg.split()[0], 0.25))
                    st.info(strength_msg)

                    # Display message for weak passwords 
                    if not strength_check:
                        st.error("Please choose a stronger password.")

                    # Display message if password not match
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        # Try registering the user
                        if register_user(new_username, new_password, role=selected_role):

                            # Display ballons and success message 
                            st.balloons()
                            st.success(f"✅ Account created with role '{selected_role}'! You can now log in.")

                            # Automatically switch to Login tab 
                            st.session_state.active_tab = "Login"
                            st.session_state.account_created = True
                        else:
                            # Display error message
                            st.error("❌ Registration failed. Try again.")
