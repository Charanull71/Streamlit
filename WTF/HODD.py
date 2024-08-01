import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

# Mapping table names to collection names
table_mapping = {
    "Theory Courses Handled": "l1",
    "Student Project Works Undertaken": "l2",
    "Student Training Activities": "l3",
    "Learning Material": "l4",
    "Certificates Courses Done": "l5",
    "FDPs Attended": "l6",
    "FDPs Organized": "l7",
    "Memberships with Professional Bodies": "l8",
    "Chairing Sessions & Delivering Talks and Lectures": "l9",
    "Journal Publications": "l10",
    "Conference Publications": "l11",
    "Research Guidance": "l12",
    "Book Publications": "l13",
    "Patents": "l14",
    "Product Design/Software Development": "l15",
    "Consultancy": "l16",
    "Funded Projects": "l17",
    "Fellowship/Award": "l18",
    "Ph.D. Details": "l19",
    "Leaves Availed": "l20"
}

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
        table = st.selectbox("Select Table", list(table_mapping.keys()))
        
        # Date filter inputs
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            collection_name = table_mapping[table]
            collection = db[collection_name]
            
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

# To run the app, call the main function with the username
# main("example_username")
