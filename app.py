import streamlit as st

# Initialize session state to store applications if it doesn't exist
if 'applications' not in st.session_state:
    st.session_state.applications = []

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
        
        # When form is submitted, add the structured data to session state
        if submit_button:
            new_app = {
                "Company": company,
                "Role": role,
                "Salary": salary,
                "Stage": stage,
                "Date Applied": date_applied.strftime("%Y-%m-%d"),
                "Job Link": job_link
            }
            st.session_state.applications.append(new_app)
            st.success("Application added successfully!")

# 2. Main area to display applications
st.header("Your Applications")

if st.session_state.applications:
    # Streamlit automatically renders a list of dictionaries as a nice table
    st.dataframe(st.session_state.applications, use_container_width=True)
else:
    st.info("No applications added yet. Use the sidebar to add one!")
