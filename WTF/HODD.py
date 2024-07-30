import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())

def main(username):
    hod_user = db['users'].find_one({"username": username, "role": "HOD"})
    
    if not hod_user:
        st.error("HOD user not found")
        return

    hod_department = hod_user.get("department")
    
    st.title(f"Retrieve Data for Department: {hod_department.upper()}")
    
    with st.form("retrieve_form"):
        table = st.selectbox("Select Table",
         [ "Theory Courses Handled",
           "Student Project Works Undertaken", 
           "Student Training Activities", 
           "Learning Material", 
           "Certificates Courses Done", 
           "FDPs Attended",
            "FDPs Organized",
            "Memberships with Professional Bodies",
            "Chairing Sessions & Delivering Talks and Lectures",
            "Journal Publications",
            "Conference Publications",
            "Research Guidance",
            "Book Publications",
            "Patents",
            "Product Design/Software Development",
            "Consultancy",
            "Funded Projects",
            "Fellowship/Award",
            "Ph.D. Details",
            "Leaves Availed"])
        
        # Date filter inputs
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            collection = db[table]
            
            # Use regex to make the department query case-insensitive
            query = {"department": {"$regex": hod_department, "$options": "i"}}
            
            # Apply date filter to query
            if start_date and end_date:
                start_datetime = date_to_datetime(start_date)
                end_datetime = date_to_datetime(end_date)
                query["date"] = {"$gte": start_datetime, "$lte": end_datetime}
            
            result = list(collection.find(query))
            
            if result:
                df = pd.DataFrame(result)
                st.write(df)
            else:
                st.write(f"No records found in {table} for department: {hod_department}")

# Example usage in the main app
# if st.session_state.role == "HOD":
#     nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Sent", "Retrieved Data", "Retrieve All Data", "Departmental Retrieve"])

#     if nav == "Departmental Retrieve":
#         import WTF.HODD as HODD
#         HODD.main(st.session_state.username)
