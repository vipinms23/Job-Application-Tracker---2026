import streamlit as st
import database as db

# Initialize the database
db.init_db()

st.title("Job Application Tracker")

# 1. Sidebar form to add new applications
with st.sidebar:
    st.header("Add New Application")
    # clear_on_submit clears the fields after a successful submission
    with st.form("add_app_form", clear_on_submit=True):
        company = st.text_input("Company")
        role = st.text_input("Role")
        salary = st.text_input("Salary")
        stage = st.selectbox("Stage", ["Applied", "OA", "Interview", "Offer", "Rejected"])
        date_applied = st.date_input("Date Applied")
        job_link = st.text_input("Job Link")
        
        submit_button = st.form_submit_button("Add Application")
        
        # When form is submitted, add the structured data to the database
        if submit_button:
            db.add_application(
                company=company,
                role=role,
                salary=salary,
                stage=stage,
                applied_on=date_applied.strftime("%Y-%m-%d"),
                link=job_link
            )
            st.success("Application added successfully!")

# 2. Main area to display applications
st.header("Your Applications")

# Fetch applications from the database
applications = db.get_all_applications()

if applications:
    # Streamlit automatically renders a list of dictionaries as a nice table
    st.dataframe(applications, use_container_width=True)
else:
    st.info("No applications added yet. Use the sidebar to add one!")
