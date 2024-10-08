import streamlit as st
from pymongo import MongoClient
import datetime
import base64
import pandas as pd
from .l1 import pascal_case  # Make sure this import is correct and relevant

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l11']  # Replace 'l11' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def calculate_points(event_type):
    points_dict = {
        "Chaired or Co-chaired (International)": 100,
        "Chaired or Co-chaired (National)": 80,
        "Delivering talks & Lectures (International)": 90,
        "Delivering talks & Lectures (National IIT/NIT Level)": 70,
        "Delivering talks & Lectures (University Level)": 50,
        "Delivering talks & Lectures (College Level)": 40
    }
    return points_dict.get(event_type, 0)

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    with st.form("l11"):
        st.title("Chairing Sessions & Delivering Talks and Lectures")

        st.write("No. Of Chairing sessions and delivering talks & lectures up to previous assessment year:")
        col1, col2, col3 = st.columns(3)
        with col1:
            lec = st.text_input("Lectures", value="", placeholder="Enter Lectures")
        with col2:
            dtalk = st.text_input("Delivering Talks", value="", placeholder="Enter Delivering Talks")
        with col3:
            ctalks = st.text_input("Chairing Talks", value="", placeholder="Enter Chairing Talks")

        st.write("No. Of Chairing sessions and delivering talks & lectures in present assessment year:")
        event_type = st.selectbox("Geographical Level of platform of delivery", [
            "", "Chaired or Co-chaired (International)", "Chaired or Co-chaired (National)", 
            "Delivering talks & Lectures (International)", "Delivering talks & Lectures (National IIT/NIT Level)", 
            "Delivering talks & Lectures (University Level)", "Delivering talks & Lectures (College Level)"
        ])
        
        Subject3 = st.text_input("Inside or out campus", value="", placeholder="Enter Inside or Out Campus")
        Subject1 = st.text_input("Name of the platform", value="", placeholder="Enter Platform Name")
        Subject4 = st.text_input("Type of delivery", value="", placeholder="Enter Type of Delivery")

        st.write("Have you delivered any guest or expert LECTURE?")
        Subject11 = st.text_input("Host institution details", value="", placeholder="Enter Host Institution Details")
        Subject13 = st.text_input("Who are the audience", value="", placeholder="Enter Audience Details")
        Subject21 = st.text_input("Type of guest or expert lecture delivered", value="", placeholder="Enter Type of Delivery")

        # File uploader for PDF
        file_uploader = st.file_uploader("Upload your all work in PDF", type=["pdf"])

        # Calculate points based on selected event type
        points = calculate_points(event_type)

        # Fetch and display dynamically added inputs (if any)
        custom_inputs = get_custom_inputs("l11")
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
            if not (lec and dtalk and ctalks and event_type and Subject3 and Subject1 and Subject4 and Subject11 and Subject13 and Subject21):
                st.error("Please fill out all required fields.")
                return

            if not file_uploader:
                st.error("Please upload your PDF.")
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
                pdf_content = file_uploader.read()
                encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

                data = {
                    "username": username,
                    "lectures": pascal_case(lec),
                    "delivering_talks": pascal_case(dtalk),
                    "chairing_talks": pascal_case(ctalks),
                    "geographical_level": event_type,
                    "inside_or_out_campus": pascal_case(Subject3),
                    "platform_name": pascal_case(Subject1),
                    "delivery_type": pascal_case(Subject4),
                    "host_institution_details": pascal_case(Subject11),
                    "audience_details": pascal_case(Subject13),
                    "guest_lecture_delivery_type": pascal_case(Subject21),
                    "certificate_pdf": encoded_pdf,
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

        st.subheader("Chairing Sessions & Lectures Delivered This Year")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username", "certificate_pdf"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")

if __name__ == "__main__":
    main(st.session_state.username)
