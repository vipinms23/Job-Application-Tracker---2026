import streamlit as st
import database as db

# Initialize the database
db.init_db()

st.title("Job Application Tracker")

# --- Dashboard Stats ---
stats = db.get_dashboard_stats()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applications", stats["total"])
col2.metric("Interviews", stats["interviews"])
col3.metric("Offers", stats["offers"])
col4.metric("Response Rate", f"{stats['response_rate']:.1f}%")

st.divider()

# --- Sidebar ---
with st.sidebar:
    st.header("Filters")
    filter_stage = st.selectbox("Filter by Stage", ["All", "Applied", "Online Assessment", "Interview", "Offer", "Rejected"])
    search_text = st.text_input("Search Company/Role")
    
    st.divider()
    
    st.header("Add New Application")
    with st.form("add_app_form", clear_on_submit=True):
        company = st.text_input("Company")
        role = st.text_input("Role")
        salary = st.text_input("Salary")
        stage = st.selectbox("Stage", ["Applied", "Online Assessment", "Interview", "Offer", "Rejected"])
        date_applied = st.date_input("Date Applied")
        job_link = st.text_input("Job Link")
        
        submit_button = st.form_submit_button("Add Application")
        
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
            st.rerun()

# --- Main List ---
st.header("Your Applications")

applications = db.get_all_applications(stage_filter=filter_stage, search_text=search_text)

if applications:
    # Header row
    h_col1, h_col2, h_col3, h_col4, h_col5, h_col6 = st.columns([2, 2, 1, 2, 2, 1])
    h_col1.write("**Company**")
    h_col2.write("**Role**")
    h_col3.write("**Salary**")
    h_col4.write("**Applied On**")
    h_col5.write("**Stage**")
    h_col6.write("**Action**")
    
    for app in applications:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 2, 1])
        
        col1.write(app["Company"])
        if app["link"]:
            col2.markdown(f"[{app['Role']}]({app['link']})")
        else:
            col2.write(app["Role"])
            
        col3.write(app["Salary"])
        col4.write(app["applied_on"])
        
        # Dropdown to change stage
        stages = ["Applied", "Online Assessment", "Interview", "Offer", "Rejected"]
        current_index = stages.index(app["stage"]) if app["stage"] in stages else 0
        new_stage = col5.selectbox(
            "Stage", 
            stages, 
            index=current_index,
            key=f"stage_{app['ID']}",
            label_visibility="collapsed"
        )
        
        # If the stage has changed, update DB and rerun
        if new_stage != app["stage"]:
            db.update_application_stage(app["ID"], new_stage)
            st.rerun()
            
        # Delete button
        if col6.button("Delete", key=f"del_{app['ID']}"):
            db.delete_application(app["ID"])
            st.rerun()
else:
    st.info("No applications found.")
