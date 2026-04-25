# ====================
# Required Imports
# ====================

from app.data.datasets import (
    get_all_datasets, list_datasets_by_source,
    display_resource_usage, get_quality_issues
)
from app.data.tickets import (
    get_all_tickets, get_ticket_trend,
    get_ticket_delays
)
from app.data.incidents import (
    get_all_incidents, get_incidents_by_type_count,
    get_incident_trend, unresolved_incidents_by_type,

)
from app.data.schema import create_all_tables
from app.data.db import connect_database
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import sys
import os

# ====================
# Path setup
# ====================

# Find the main project directory, facilitating local module imports
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

# ==============================
# Import required local modules
# ==============================


# Import Cybersecurity domain functions

# Import IT Operations domain functions

# Import Data Science domain functions
# --- LOGIN CHECK ---
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
st.set_page_config(page_title="Wave - Analytics",
                   layout="wide", page_icon="assets/logo.png")

# Display banner
st.image("C:\\CW2\\CW2_CST1510_M01041173_COMPLETE_VERSION-main\\project\\\\assets\\banner3.png", caption="banner image", use_container_width=True)

# Domain selection
domain_options = st.sidebar.selectbox(
    "Select Domain", ["Cybersecurity", "IT Operations", "Data Science"])

# Define paths for the database directory and file
PROJECT_DATA_DIR = os.path.join(PROJECT_ROOT, "DATA")
DB_FILE = os.path.join(PROJECT_DATA_DIR, "intelligence_platform.db")

# Establish a connection to the database
conn = connect_database(DB_FILE)
create_all_tables(conn)  # create all required tables

# Fetch data from database tables into global variables
df_incidents = get_all_incidents(conn)
df_datasets = get_all_datasets(conn)
df_tickets = get_all_tickets(conn)


# ----- View records function -----
def view_records(conn, domain):

    # Custom CSS styling to tables and headers
    st.markdown("""
    <style>
    .table-header {font: bold 26px "Segoe UI", Roboto, sans-serif; color:#0b3d91; border-bottom:3px solid #ff4b4b; margin-bottom:10px;}
    th {background:#0b3d91; color:#fff; padding:8px;}
    td {padding:6px; border-bottom:1px solid #ddd;}
    tr:hover {background:#f1f1f1;}
    </style>
    """, unsafe_allow_html=True)

    # Display Cybersecurity incidents with filtering options
    if domain == "Cybersecurity":

        # Display Decorated header
        st.markdown(
            '<div class="table-header">🔒 Cyber Incidents</div>', unsafe_allow_html=True)

        # Provide filtering options for severity
        incidents_severity_filter = st.multiselect(
            "Select Severity", ["Low", "Medium", "High", "Critical"],
            default=["Low", "Medium", "High", "Critical"]
        )

        # Provide filtering options for status
        status_filter = st.multiselect(
            "Select Status", ["Open", "Investigating", "Resolved", "Closed"],
            default=["Open", "Investigating", "Resolved", "Closed"]
        )

        # Apply filters to the incidents table
        filtered_df = df_incidents[
            df_incidents["severity"].isin(incidents_severity_filter) &
            df_incidents["status"].isin(status_filter)
        ]

        # Display number of filtered records
        st.caption(f"{len(filtered_df)} incidents after filtering.")

        # Display filtered incidents in a expander
        with st.expander("Filtered Incidents"):
            st.dataframe(filtered_df, use_container_width=True)

    # Display IT Operations with filtering options
    elif domain == "IT Operations":

        # Display Decorated header
        st.markdown('<div class="table-header">💻 IT Tickets</div>',
                    unsafe_allow_html=True)

        # Provide filtering options for priority
        priority_filter = st.multiselect(
            "Select Priority", ["Low", "Medium", "High", "Critical"],
            default=["Low", "Medium", "High", "Critical"]
        )

        # Provide filtering options for status
        status_filter = st.multiselect(
            "Select Status", ["Open", "Investigating", "Resolved", "Closed"],
            default=["Open", "Investigating", "Resolved", "Closed"]
        )

        # Apply filters to the tickets table
        filtered_df = df_tickets[
            df_tickets["priority"].isin(priority_filter) &
            df_tickets["status"].isin(status_filter)
        ]

        # Display number of filtered records
        st.caption(f"{len(filtered_df)} tickets after filtering.")

        # Display filtered tickets in a expander
        with st.expander("Filtered Tickets"):
            st.dataframe(filtered_df, use_container_width=True, height=600)

    # Display Data Science with filtering options
    elif domain == "Data Science":

        # Display Decorated header
        st.markdown(
            '<div class="table-header">📊 Data Science Datasets</div>', unsafe_allow_html=True)

        # Convert column to datetime format
        df_datasets["last_updated"] = pd.to_datetime(
            df_datasets["last_updated"], errors="coerce")

        # Provide filtering options for category
        category_filter = st.multiselect(
            "Category",
            df_datasets["category"].unique(),
            default=df_datasets["category"].unique()
        )

        # Provide Filtering option by record count using a slider
        min_records = int(df_datasets["record_count"].min())
        max_records = int(df_datasets["record_count"].max())
        record_range = st.slider(
            "Record Count Range", min_value=min_records, max_value=max_records, value=(min_records, max_records)
        )

        # Apply filters to the datasets table
        filtered_df = df_datasets[
            df_datasets["category"].isin(category_filter) &
            df_datasets["record_count"].between(
                record_range[0], record_range[1])
        ]

        # Display number of filtered datasets
        st.caption(f"{len(filtered_df)} datasets after filtering.")

        # Display filtered datasets in a expander
        with st.expander("Filtered Datasets"):
            st.dataframe(filtered_df, use_container_width=True)

# ---- Domain Visulization function ----


def domain_visualization():

    # ---------------- Cybersecurity Domain ----------------
    if domain_options == "Cybersecurity":

        # Create tabs to display visulizations
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Overview", "Bar Charts", "Line Charts", "Heatmaps"])

        # Overview tab
        with tab1:
            # Display decorated header
            st.markdown(
                "<h3 style='text-align: center;'>Cybersecurity Threat Insights</h3>", unsafe_allow_html=True)

            # Call fucntion to display records
            view_records(conn, domain_options)

            # Convert column to datetime format
            df_incidents["date"] = pd.to_datetime(
                df_incidents["date"], errors="coerce", dayfirst=False)

            # Define last two dates in the dataset
            latest_date = df_incidents["date"].max()
            previous_date = latest_date - pd.Timedelta(days=1)

            # Compute counts for previous day
            previous_total = len(
                df_incidents[df_incidents["date"] == previous_date])
            previous_vulnerability = len(df_incidents[(
                df_incidents["date"] == previous_date) & df_incidents["severity"].isin(["High", "Critical"])])
            previous_active = len(df_incidents[(
                df_incidents["date"] == previous_date) & df_incidents["status"].isin(["Open", "Investigating"])])

            # Compute Current counts
            current_total = len(
                df_incidents[df_incidents["date"] == latest_date])
            current_vulnerability = len(
                df_incidents[df_incidents["severity"].isin(["High", "Critical"])])
            current_active = len(
                df_incidents[df_incidents["status"].isin(["Open", "Investigating"])])

            # Display KPI with deltas
            col1, col2, col3 = st.columns(3)
            col1.metric("Threats Detected", current_total,
                        delta=f"{current_total - previous_total:+d}")
            col2.metric("High-Risk Vulnerabilities", current_vulnerability,
                        delta=f"{current_vulnerability - previous_vulnerability:+d}")
            col3.metric("Active Incidents", current_active,
                        delta=f"{current_active - previous_active:+d}")

        # Bar charts tab
        with tab2:

            # Display Header
            st.subheader("Cybersecurity Threat Insights")

            # 1) Bar Chart: Incidnets Type count

            # Get Incidnets Type count
            incidents_type_count = get_incidents_by_type_count(conn)

            # Create bar chart
            bar_chart = px.bar(
                incidents_type_count, x="incident_type", y="count", color="incident_type",
                title="Total Incidents by Type", text="count"
            )

            # Display Graph
            st.plotly_chart(bar_chart, use_container_width=True)

            # 2) Bar Chart: Unresolved incidents Type count
            unresolved_incidents = unresolved_incidents_by_type(conn)

            # Create bar chart
            bar_chart = px.bar(
                unresolved_incidents, x="incident_type", y="unresolved_cases", color="incident_type",
                title="Unresolved Incidents by Type", text="unresolved_cases"
            )
            #  Display Graph
            st.plotly_chart(bar_chart, use_container_width=True)

        # Line Chart tab
        with tab3:

            # Get incidnet trend
            df = get_incident_trend(conn)

            # Display a line chart of total incidents by type
            st.altair_chart(
                alt.Chart(df).mark_line(point=True).encode(
                    x='incident_type', y='total_incidents',
                    tooltip=['incident_type', 'total_incidents']
                ).properties(height=400, title='Incident Trends by Type'),
                use_container_width=True
            )

            # Compute Phising Incident trend over months
            phishing_trend = (
                df_incidents[df_incidents["incident_type"] == "Phishing"]
                .assign(date=pd.to_datetime(df_incidents["date"], dayfirst=True, errors="coerce"))
                .groupby(pd.Grouper(key="date", freq="M"))
                .size()
                .reset_index(name='count')

            )

            # Display a line chart of Phishing incidents over time
            st.plotly_chart(
                px.line(
                    phishing_trend,
                    x="date",
                    y="count",
                    markers=True,
                    title="📈 Phishing Incidents Over Time",
                    labels={'date': 'Month',
                            'count': 'Number of Phishing Incidents'}
                ),
                use_container_width=True
            )

        # Heatmaps tab
        with tab4:

            # Select required columns
            df = df_incidents[['incident_type', 'severity']]

            # Compute counts
            heatmap_data = df.groupby(
                ['incident_type', 'severity']).size().reset_index(name='count')

            # Create heatmap of incident severity by type
            heatmap = alt.Chart(heatmap_data).mark_rect().encode(
                x='incident_type', y='severity',
                color=alt.Color('count', scale=alt.Scale(scheme='reds')),
                tooltip=['incident_type', 'severity', 'count']
            ).properties(height=400, title='Heatmap of Cyber Incidents')

            # Display heatmap
            st.altair_chart(heatmap, use_container_width=True)

    # ---------------- IT Operations Domain ----------------
    elif domain_options == "IT Operations":

        # Get ticket delays and trends
        staff_delays_df, status_delays_df = get_ticket_delays(conn)
        ticket_trend_df = get_ticket_trend(conn)

        # Create tabs to display visulizations
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Overview", "Bar Charts", "Line Charts", "Other"])

        # Overview tab
        with tab1:
            # Display decorated header
            st.markdown(
                "<h3 style='text-align: center;'>IT Ticket Insights</h3>", unsafe_allow_html=True)

            # Call fucntion to display records
            view_records(conn, domain_options)

            # Display ticket metrics in three columns
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tickets", len(df_tickets))
            col2.metric("Unresolved Tickets",
                        df_tickets["resolved_date"].isna().sum())
            col3.metric("High Priority",
                        (df_tickets["priority"] == "High").sum())

        # Bar charts tab
        with tab2:

            # Display Header
            st.subheader("IT Ticket Delay Insights")

            # Bar chart: Unresolved tickets by staff
            bar_chart = alt.Chart(staff_delays_df).mark_bar().encode(
                x="assigned_to", y="unresolved_count", tooltip=["assigned_to", "unresolved_count"]
            ).properties(title="Unresolved Tickets by Staff", height=350)

            # Display Graph
            st.altair_chart(bar_chart, use_container_width=True)

            # Bar chart: Unresolved tickets by status
            bar_chart = alt.Chart(status_delays_df).mark_bar().encode(
                x="status", y="unresolved_count"
            ).properties(title="Unresolved Tickets by Status", height=350)

            # Display Graph
            st.altair_chart(bar_chart, use_container_width=True)

            # Bar chart: Ticket priority distribution
            priority_df = df_tickets.groupby(
                "priority").size().reset_index(name="count")
            priority_chart = alt.Chart(priority_df).mark_bar().encode(
                x="priority", y="count"
            ).properties(title="Ticket Priority Distribution", height=350)

            #  Display Graph
            st.altair_chart(priority_chart, use_container_width=True)

        # Line Chart tab
        with tab3:

            # Create Daily Ticket Creation Trend
            line_chart = alt.Chart(ticket_trend_df).mark_line(point=True).encode(
                x="created_date", y="Tickets Created"
            ).properties(height=350, title="Daily Ticket Creation Trend")

            # Display graph
            st.altair_chart(line_chart, use_container_width=True)

        # Cumulative resolved tickets graph
        with tab4:

            # Decorative Header
            st.subheader("Cumulative Tickets Resolved Over Time")

            # Convert dates and calculate cumulative resolved tickets
            df_tickets['resolved_date'] = pd.to_datetime(
                df_tickets['resolved_date'], errors='coerce')
            resolved_trend = df_tickets.dropna(subset=['resolved_date']).groupby(
                'resolved_date').size().cumsum().reset_index(name='Cumulative Resolved')

            # Create and Display line chart
            cumulative_line = alt.Chart(resolved_trend).mark_line(point=True, color="#9467bd").encode(
                x='resolved_date', y='Cumulative Resolved'
            ).properties(height=300)

            st.altair_chart(cumulative_line, use_container_width=True)

            # Compute tickets by priority
            priority_counts = df_tickets['priority'].value_counts(
            ).reset_index()
            priority_counts.columns = ['priority', 'count']

            # Plot pie chart for ticket priority distribution
            fig = px.pie(
                priority_counts, names='priority', values='count',
                hole=0.5,
                color_discrete_map={'Low': '#1f77b4', 'Medium': '#ff7f0e', 'High': '#d62728', 'Critical': '#9467bd'}, title='Ticket Priority Distribution'
            )

            # Decorate pie chart
            fig.update_traces(
                textinfo='percent+label',
                marker=dict(line=dict(color='#000000', width=2))
            )
            st.plotly_chart(fig, use_container_width=True)

# ---------------- Data Science Domain ----------------
    elif domain_options == "Data Science":

        # Create tabs to display visulizations
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Overview", "Storage", "Distribution", "Explorer"])

        # Overview tab
        with tab1:

            # Display decorated header
            st.markdown(
                "<h3 style='text-align: center;'>Data Science Insights</h3>", unsafe_allow_html=True)

            # Convert 'last_updated' to datetime and get previous records
            df_datasets["last_updated"] = pd.to_datetime(
                df_datasets["last_updated"], errors="coerce")
            previous_df = df_datasets[df_datasets["last_updated"]
                                      < df_datasets["last_updated"].max()]

            # Calculate previous total records and file size
            previous_total_records = previous_df["record_count"].sum()
            previous_total_size_mb = previous_df["file_size_mb"].sum()

            # Calculate current total records and file size
            total_records = df_datasets["record_count"].sum()
            total_size_mb = df_datasets["file_size_mb"].sum()

            # Display KPIs with deltas
            col1, col2, col3 = st.columns(3)
            col1.metric("Datasets", len(df_datasets),
                        delta=f"{len(df_datasets) - len(previous_df):+d}")
            col2.metric("Total Records", total_records,
                        delta=f"{total_records - previous_total_records:+d}")
            col3.metric("Total Size (MB)", f"{total_size_mb:.1f}",
                        delta=f"{total_size_mb - previous_total_size_mb:+.1f}")

        # ---  Storage & Resource Usage tab
        with tab2:

            # Display decorated header
            st.markdown(
                "<h3 style='text-align: center;'>Top Resource-Consuming Datasets</h3>", unsafe_allow_html=True)

            # Fetch dataset and get resource usage
            resource_usage = display_resource_usage(conn)

            # Calculate & Display top 10 datasets in a table
            df_usage = resource_usage.head(10)
            st.dataframe(df_usage, use_container_width=True)

            # Display Bar chart of top datasets by file size
            fig = px.bar(
                resource_usage.head(10),
                x="dataset_name",
                y="file_size_mb",
                title="Top Datasets by File Size (MB)",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            # Save top 10 datasets to CSV
            file_path = "top_datasets.csv"
            df_usage.to_csv(file_path, index=False)

            # Provide download button
            with open(file_path, "rb") as f:
                st.download_button("Download Top 10 Datasets CSV",
                                   f, file_name="top_datasets.csv", mime="text/csv")

        # ----TAB 3: Distribution ----
        with tab3:

            # Display decorated header
            st.markdown(
                "<h3 style='text-align: center;'>Dataset Source & Category Breakdown</h3>", unsafe_allow_html=True)

            # Fetch dataset sources
            df_sources = list_datasets_by_source(conn)

            # Create tabs for visualization
            tab1, tab2 = st.tabs(
                ["Datasets by Source", "Category Distribution"])

            # Bar chart of datasets by source
            with tab1:
                fig = px.bar(df_sources, x="source", y="dataset_count",
                             title="Datasets by Source", height=450)
                st.plotly_chart(fig, use_container_width=True)

            # Tab 2: Pie chart of dataset categories
            with tab2:
                # Convert value_counts from Series to DataFrame
                category_counts = (
                    df_datasets["category"]
                    .value_counts()
                    .reset_index()
                )
                category_counts.columns = ["category", "count"]

                # Display pie chart
                fig = px.pie(
                    category_counts,
                    names="category",
                    values="count",
                    title="Category Distribution",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)

        # Display Records Tab
        with tab4:

            # Show records for the selected domain
            view_records(conn, domain_options)


# Run function
domain_visualization()

# --- LOGOUT ---
st.divider()

# Logout button
if st.button("Log Out"):

    # Update login state
    st.session_state.logged_in = False
    # Display success message
    st.success("Logged out!")
    # Redirect user to Home page
    st.switch_page("Home.py")
