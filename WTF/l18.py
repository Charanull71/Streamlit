import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd
from .l1 import pascal_case  # Ensure this import is correct and relevant

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l18']  # Replace 'l18' with your actual collection name
collection_users = db['users']
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

# Define points for each position in the team
def calculate_points(position):
    POSITION_POINTS = {
        "Single": 100,
        "First or Principle person": 50,
        "Other Persons": 10
    }
    return POSITION_POINTS.get(position, 0)

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    with st.form("l18"):
        st.title("CONSULTANCY")

        n1 = st.text_input("Total Consultancy upto previous assessment year: (in Rs.)")
        
        st.write("Consultancy in present assessment year:")
        toc = st.text_input("Title of Consultancy work", value="", placeholder="Enter Title of Consultancy work")
        
        nga = st.text_input("Name of Granting Agency", value="", placeholder="Name of Granting Agency")
        
        nci = st.text_input("No of Coordinators involved", value="", placeholder="Enter No of Coordinators involved")
        
        # Dropdown for position in the team
        poc = st.selectbox("Position in order of coordinatorship", options=["Single", "First or Principle person", "Other Persons"])
        poc_points = calculate_points(poc)
        
        sin = st.date_input("Since:", datetime.datetime.now(), format="MM.DD.YYYY")
        
        gm = st.text_input("Grant/Amount mobilised", value="", placeholder="Enter Grant/Amount mobilised")

        # Fetch and display dynamically added inputs (e.g., media, dropdowns)
        custom_inputs = get_custom_inputs("l18")
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
            if not (n1 and toc and nga and nci and gm):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                sin = datetime.datetime.combine(sin, datetime.datetime.min.time())
                username = st.session_state.username  # Replace with your actual way of getting username
                
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                data = {
                    "username": username,
                    "total_consultancy_previous": n1,
                    "title_consultancy_work": pascal_case(toc),
                    "granting_agency": pascal_case(nga),
                    "coordinators_involved": nci,
                    "position_coordinatorship": poc,
                    "position_points": poc_points,
                    "since_date": sin,
                    "grant_amount_mobilised": gm,
                    "department": department,
                    "date": datetime.datetime.now()
                }

                # Add custom inputs to the data dictionary
                data.update(additional_data)

                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.subheader("Consultancy This Year")
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
