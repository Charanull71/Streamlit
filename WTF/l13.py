import streamlit as st
from pymongo import MongoClient
import datetime
import base64
import pandas as pd
from .l1 import pascal_case

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l13']  # Replace 'l13' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def calculate_conference_points(proceeding_type, venue_location, authorship_position, venue_level):
    points_dict = {
        "IEEE/Springer or equivalent": {
            "India": {
                "> University Level": {"1st author": 80, "other": 10},
                "University Level": {"1st author": 70, "other": 10},
                "College Level": {"1st author": 60, "other": 5}
            },
            "Abroad": {
                "> University Level": {"1st author": 100, "other": 20},
                "University Level": {"1st author": 90, "other": 20},
                "College Level": {"1st author": 80, "other": 10}
            }
        },
        "Other Conferences": {
            "India": {
                "> University Level": {"1st author": 40, "other": 5},
                "University Level": {"1st author": 30, "other": 5},
                "College Level": {"1st author": 20, "other": 5}
            },
            "Abroad": {
                "> University Level": {"1st author": 50, "other": 10},
                "University Level": {"1st author": 40, "other": 10},
                "College Level": {"1st author": 30, "other": 5}
            }
        }
    }
    return points_dict.get(proceeding_type, {}).get(venue_location, {}).get(venue_level, {}).get(authorship_position, 0)

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    with st.form("l13"):
        st.title("Conference Publications for Current Assessment Year")

        st.write("Conference Publication Details")
        ath = st.text_input("No. of Authors", value="", placeholder="Enter Number of Authors")
        pat = st.selectbox("Position of Authorship", ["", "1st author", "other"])
        pven = st.text_input("Venue of Conference", value="", placeholder="Enter Conference Venue")
        Jtype = st.selectbox("Venue Location", ["", "India", "Abroad"])
        ptype = st.selectbox("Proceedings Type", ["", "IEEE/Springer or equivalent", "Other Conferences"])
        venue_level = st.selectbox("Venue Level", ["", "> University Level", "University Level", "College Level"])
        
        # File uploader for PDF
        pdf_uploader = st.file_uploader("Upload your work in PDF", type=["pdf"])

        # Fetch and display dynamically added inputs
        custom_inputs = get_custom_inputs("l13")
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
            if not (ath and pat and pven and Jtype and ptype and venue_level):
                st.error("Please fill out all required fields.")
                return

            if not pdf_uploader:
                st.error("Please upload the PDF.")
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
                pdf_content = pdf_uploader.read()
                encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

                # Calculate points
                points = calculate_conference_points(ptype, Jtype, pat, venue_level)

                data = {
                    "username": username,
                    "number_of_authors": ath,
                    "position_of_authorship": pat,
                    "conference_venue": pascal_case(pven),
                    "venue_location": Jtype,
                    "proceedings_type": ptype,
                    "venue_level": venue_level,
                    "pdf": encoded_pdf,
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

    st.subheader("Conference Publications (Current Academic Year)")
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
