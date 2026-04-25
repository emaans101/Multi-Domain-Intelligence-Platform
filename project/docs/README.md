# CW2_CST1510_M01041173

# Week 9 & 10: Interactive Multi-Domain Dashboard (Streamlit + AI)
Student Name: Emaan Fatima  
Student ID: M01041173  
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
This project builds upon the Week 8 SQLite-based CRUD system by providing a **fully interactive web dashboard using Streamlit**. Users can securely register, log in, and interact with multiple data domains (Cybersecurity, IT Operations, Data Science) via a **user-friendly GUI**.  

The dashboard supports **viewing, adding, updating, and deleting records** with real-time validation and role-based access.  

- **Week 9:** Added domain-specific **visualization pages**, allowing users to explore insights and graphs from each domain.  
- **Week 10:** Integrated **AI-powered assistance**, enabling users to interact with a domain-specific chatbot to query records, analyze data, and receive actionable insights.

## Features
- **Secure Authentication System:**
  - User registration with password validation and strength checking
  - Login with session management
  - Role selection (`user`, `admin`, `analyst`)
- **Interactive Multi-Domain Dashboard:**
  - Domains: Cybersecurity, IT Operations, Data Science
  - Sidebar for selecting domains and CRUD options
  - Dynamic forms to add new records
  - Update/Delete functionality with controlled editable fields
- **Interactive Multi-Domain Visualization:**
  - Users can select a domain and access charts, graphs, and insights
  - Tabs for domain-specific visualizations

- **Interactive Multi-Domain AI Assistance:**
  - Domain-specific chatbot for querying incidents, tickets, or datasets
  - Chat history stored per domain
  - Option to clear chat and download conversation
  - Model selection and temperature adjustment for AI responses
- **Record Management:**
  - View existing records in styled tables
  - Add new records using Streamlit forms
  - Update or delete records safely with database constraints
- **Data Persistence:**
  - SQLite database stores users, incidents, datasets, and IT tickets

- **User Experience Enhancements:**
  - Real-time feedback messages and success indicators
  - Password strength meter with visual progress bar
  - Automatic session handling and page redirection
  - Friendly banners, icons, and structured layout

## Technical Implementation
- **Web Framework:** Streamlit
- **Database:** SQLite3
- **Data Loading:** pandas for CSV import
- **Authentication:** Python functions with file-based user management (`users.txt`) or database-backed sessions
- **CRUD Functions:** Custom Python functions in `utils.py`
- **AI Integration:** OpenAI API for domain-specific assistant
- **UI Features:**
  - Selectboxes, multiselect, radio buttons, and forms
  - Domain-specific options with editable fields
  - Custom CSS styling for tables and headers
  
- **Folder Structure:**
  - `DATA/` → CSV files, SQLite database, user file, session file
  - `assets/` → Banner images and icons
  - `app/data/` → Database helper functions and schema
  - `project/utils.py` → Reusable CRUD functions
  - `pages/` → Streamlit app pages
  - `authentication/` → User authentication registration and login modules
  - `project/Home.py` → Home page for app

## Beginner Tip
Think of this Streamlit dashboard as a **smart Excel file that comes to life**:
- Lives on disk (persists data)
- Lets you **add, update, or remove records safely**
- Allows domain-specific access (Cybersecurity, IT, Data Science)
- Provides **real-time visual feedback** and interactive forms
- Integrates **AI assistance and visualizations** for deeper insights
- Protects data integrity and prevents SQL injection
