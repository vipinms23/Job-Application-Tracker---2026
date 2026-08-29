import streamlit as st
import database as db
import analyzer as anlz

# Initialize the database
db.init_db()

st.title("Job Application Tracker")

tab1, tab2 = st.tabs(["Dashboard", "JD Analyzer"])

with tab1:
    # --- Dashboard Stats ---
    stats = db.get_dashboard_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Applications", stats["total"])
    col2.metric("Interviews", stats["interviews"])
    col3.metric("Offers", stats["offers"])
    col4.metric("Response Rate", f"{stats['response_rate']:.1f}%")

    st.divider()

    # --- Main List ---
    st.header("Your Applications")
    
    # We need to grab search_text and filter_stage from sidebar to use here
    # Sidebar components run globally for the page, so they are fine outside the tab
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
            c1, c2, c3, c4, c5, c6 = st.columns([2, 2, 1, 2, 2, 1])
            
            c1.write(app["Company"])
            if app["link"]:
                c2.markdown(f"[{app['Role']}]({app['link']})")
            else:
                c2.write(app["Role"])
                
            c3.write(app["Salary"])
            c4.write(app["applied_on"])
            
            # Dropdown to change stage
            stages = ["Applied", "Online Assessment", "Interview", "Offer", "Rejected"]
            current_index = stages.index(app["stage"]) if app["stage"] in stages else 0
            new_stage = c5.selectbox(
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
            if c6.button("Delete", key=f"del_{app['ID']}"):
                db.delete_application(app["ID"])
                st.rerun()
    else:
        st.info("No applications found.")

with tab2:
    st.header("Job Description Analyzer")
    user_skills_text = st.text_input("Your Tech Stack (comma separated)", "python, sql, git")
    jd_text = st.text_area("Paste Job Description Here", height=200)
    
    if st.button("Analyze Match"):
        if jd_text.strip():
            user_skills_list = [s.strip() for s in user_skills_text.split(',')]
            jd_skills = anlz.extract_skills(jd_text)
            
            if jd_skills:
                result = anlz.analyze_match(jd_skills, user_skills_list)
                
                st.metric("Match Score", f"{result['match_score']}%")
                
                a_col1, a_col2 = st.columns(2)
                with a_col1:
                    st.success("Skills You Have")
                    if result["have_skills"]:
                        for s in result["have_skills"]:
                            st.write(f"- {s.title()}")
                    else:
                        st.write("None")
                with a_col2:
                    st.error("Missing Skills")
                    if result["missing_skills"]:
                        for s in result["missing_skills"]:
                            st.write(f"- {s.title()}")
                    else:
                        st.write("None")
            else:
                st.warning("No recognized skills found in this job description.")
        else:
            st.warning("Please paste a job description first.")
