import streamlit as st
import datetime
from pymongo import MongoClient
import base64
import pandas as pd
from .l1 import pascal_case  # Make sure this import is correct and relevant

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l10']  # Replace 'l10' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def calculate_points(membership_type):
    if membership_type == "International Membership":
        return 50
    elif membership_type == "National Membership":
        return 25
    return 0

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()
    
    with st.form("l10"):
        st.title("MEMBERSHIPS WITH PROFESSIONAL BODIES")
        
        professional_body = st.text_input("Professional Body", value="", placeholder="Enter Professional Body Name")
        since_date = st.date_input("Since Date", today, format="MM.DD.YYYY")
        membership_type = st.selectbox("National/International", ["", "International Membership", "National Membership"])
        
        certificate_file = st.file_uploader("Upload your role certificate PDF", type=["pdf"])

        # Calculate points based on membership type
        points = calculate_points(membership_type)

        # Fetch and display dynamically added inputs (e.g., media, dropdowns)
        custom_inputs = get_custom_inputs("l10")
        additional_data = {}

        for custom_input in custom_inputs:
            if custom_input['input_type'] == "Text":
                additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
            elif custom_input['input_type'] == "Dropdown":
                additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
            elif custom_input['input_type'] == "Media":
                additional_data[custom_input['input_name']] = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", type=["jpg", "jpeg", "png", "pdf"])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Check for empty fields
            if not professional_body or not since_date or not membership_type:
                st.error("Please fill out all required fields.")
                return
            
            if not certificate_file:
                st.error("Please upload your certificate PDF.")
                return

            try:
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                # Read the file content and encode it in base64
                certificate_content = certificate_file.read()
                encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')

                data = {
                    "username": username,
                    "professional_body": pascal_case(professional_body),
                    "since_date": since_date.strftime("%Y-%m-%d"),
                    "membership_type": membership_type,
                    "points": points,
                    "department": department,
                    "certificate_file": encoded_certificate,
                    "date": datetime.datetime.now()
                }

                # Add custom inputs to the data dictionary
                data.update(additional_data)

                collection.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        st.subheader("Memberships with Professional Bodies (Current Academic Year)")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username", "certificate_file"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")   

if __name__ == "__main__":
    main(st.session_state.username)
