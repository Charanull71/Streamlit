import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd
from .l1 import pascal_case

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l14']  # Replace 'l14' with your actual collection name
collection_users = db['users']  # Users collection for department lookup
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def calculate_guidance_points(guide_type, date_of_registration):
    current_date = datetime.datetime.now()
    duration = (current_date - date_of_registration).days / 365.25  # Convert duration to years

    if guide_type.lower() == "guide":
        if duration <= 1:
            return 100
        elif 1 < duration <= 2:
            return 75
        elif 2 < duration <= 3:
            return 50
        else:
            return 25
    elif guide_type.lower() == "co-guide":
        if duration <= 1:
            return 50
        elif 1 < duration <= 2:
            return 35
        elif 2 < duration <= 3:
            return 20
        else:
            return 0
    return 0

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    with st.form("l14"):
        st.title("RESEARCH GUIDANCE (Ph.D/M.Phil)")

        n1 = st.text_input("No. Of STUDENTS Completed Ph.D/M.Phil:")
        st.write("No. Of STUDENTS doing Ph.D/M.Phil in present assessment year:")
        col1, col2 = st.columns(2)
        with col1:
            deg = st.text_input("Degree", value="", placeholder="Enter Degree")
        with col2:
            uni = st.text_input("University", value="", placeholder="Enter University")
        
        gui = st.selectbox("Guide/Co-Guide", ["", "Guide", "Co-Guide"])
        frod3 = st.date_input("Date of Registration", datetime.datetime.now().date(), format="YYYY-MM-DD")
        stype = st.text_input("Student Particulars", value="", placeholder="Enter Particulars Of Student")

        # Fetch and display dynamically added inputs
        custom_inputs = get_custom_inputs("l14")
        additional_data = {}

        for custom_input in custom_inputs:
            if custom_input['input_type'] == "Text":
                additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
            elif custom_input['input_type'] == "Dropdown":
                additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
            elif custom_input['input_type'] == "Media":
                additional_data[custom_input['input_name']] = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", type=["jpg", "jpeg", "png", "pdf"])

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and deg and uni and gui and stype):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                frod3 = datetime.datetime.combine(frod3, datetime.datetime.min.time())
                username = st.session_state.username  # Replace with your actual way of getting username
                
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                # Calculate points
                points = calculate_guidance_points(gui, frod3)

                # Prepare data for insertion
                data = {
                    "username": username,
                    "students_completed": n1,
                    "degree": pascal_case(deg),
                    "university": pascal_case(uni),
                    "guide": gui,
                    "date_of_registration": frod3,
                    "student_particulars": stype,
                    "department": department,
                    "points": points,
                    "date": datetime.datetime.now()
                }
                # Add custom inputs to the data dictionary
                data.update(additional_data)

                collection.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.subheader("Research Guidance for Students (Ph.D/M.Phil)")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")

if __name__ == "__main__":
    main(st.session_state.username)
