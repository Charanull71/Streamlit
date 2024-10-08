import streamlit as st
import datetime
import base64
from pymongo import MongoClient
import pandas as pd
from .l1 import pascal_case  # Ensure this import is correct and relevant

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l7']  # Replace 'l7' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

# Function to get points based on FDP type, funding type, and capacity
def get_points(fdp_type, funding_type, capacity):
    points_dict = {
        # International (>=2W)
        ("International (>=2W)", "External", "Convenor"): 100,
        ("International (>=2W)", "External", "Co-convenor"): 50,
        ("International (>=2W)", "External", "Sponsor"): 90,
        ("International (>=2W)", "External", "Internal"): 80,
        ("International (>=2W)", "Sponsor", "Convenor"): 90,
        ("International (>=2W)", "Sponsor", "Co-convenor"): 45,
        ("International (>=2W)", "Sponsor", "Sponsor"): 80,
        ("International (>=2W)", "Sponsor", "Internal"): 70,
        ("International (>=2W)", "Internal", "Convenor"): 80,
        ("International (>=2W)", "Internal", "Co-convenor"): 40,
        ("International (>=2W)", "Internal", "Sponsor"): 70,
        ("International (>=2W)", "Internal", "Internal"): 60,

        # National (>=2W)
        ("National (>=2W)", "External", "Convenor"): 90,
        ("National (>=2W)", "External", "Co-convenor"): 45,
        ("National (>=2W)", "External", "Sponsor"): 80,
        ("National (>=2W)", "External", "Internal"): 70,
        ("National (>=2W)", "Sponsor", "Convenor"): 80,
        ("National (>=2W)", "Sponsor", "Co-convenor"): 40,
        ("National (>=2W)", "Sponsor", "Sponsor"): 70,
        ("National (>=2W)", "Sponsor", "Internal"): 60,
        ("National (>=2W)", "Internal", "Convenor"): 70,
        ("National (>=2W)", "Internal", "Co-convenor"): 35,
        ("National (>=2W)", "Internal", "Sponsor"): 60,
        ("National (>=2W)", "Internal", "Internal"): 50,

        # International (1W to 2W)
        ("International (1W to 2W)", "External", "Convenor"): 90,
        ("International (1W to 2W)", "External", "Co-convenor"): 45,
        ("International (1W to 2W)", "External", "Sponsor"): 80,
        ("International (1W to 2W)", "External", "Internal"): 70,
        ("International (1W to 2W)", "Sponsor", "Convenor"): 80,
        ("International (1W to 2W)", "Sponsor", "Co-convenor"): 40,
        ("International (1W to 2W)", "Sponsor", "Sponsor"): 70,
        ("International (1W to 2W)", "Sponsor", "Internal"): 60,
        ("International (1W to 2W)", "Internal", "Convenor"): 70,
        ("International (1W to 2W)", "Internal", "Co-convenor"): 35,
        ("International (1W to 2W)", "Internal", "Sponsor"): 60,
        ("International (1W to 2W)", "Internal", "Internal"): 50,

        # National (1W to 2W)
        ("National (1W to 2W)", "External", "Convenor"): 80,
        ("National (1W to 2W)", "External", "Co-convenor"): 40,
        ("National (1W to 2W)", "External", "Sponsor"): 70,
        ("National (1W to 2W)", "External", "Internal"): 60,
        ("National (1W to 2W)", "Sponsor", "Convenor"): 70,
        ("National (1W to 2W)", "Sponsor", "Co-convenor"): 35,
        ("National (1W to 2W)", "Sponsor", "Sponsor"): 60,
        ("National (1W to 2W)", "Sponsor", "Internal"): 50,
        ("National (1W to 2W)", "Internal", "Convenor"): 60,
        ("National (1W to 2W)", "Internal", "Co-convenor"): 30,
        ("National (1W to 2W)", "Internal", "Sponsor"): 50,
        ("National (1W to 2W)", "Internal", "Internal"): 40,

        # International (<1W)
        ("International (<1W)", "External", "Convenor"): 80,
        ("International (<1W)", "External", "Co-convenor"): 40,
        ("International (<1W)", "External", "Sponsor"): 70,
        ("International (<1W)", "External", "Internal"): 60,
        ("International (<1W)", "Sponsor", "Convenor"): 70,
        ("International (<1W)", "Sponsor", "Co-convenor"): 35,
        ("International (<1W)", "Sponsor", "Sponsor"): 60,
        ("International (<1W)", "Sponsor", "Internal"): 50,
        ("International (<1W)", "Internal", "Convenor"): 60,
        ("International (<1W)", "Internal", "Co-convenor"): 30,
        ("International (<1W)", "Internal", "Sponsor"): 50,
        ("International (<1W)", "Internal", "Internal"): 40,

        # National (<1W)
        ("National (<1W)", "External", "Convenor"): 70,
        ("National (<1W)", "External", "Co-convenor"): 35,
        ("National (<1W)", "External", "Sponsor"): 60,
        ("National (<1W)", "External", "Internal"): 50,
        ("National (<1W)", "Sponsor", "Convenor"): 60,
        ("National (<1W)", "Sponsor", "Co-convenor"): 30,
        ("National (<1W)", "Sponsor", "Sponsor"): 50,
        ("National (<1W)", "Sponsor", "Internal"): 40,
        ("National (<1W)", "Internal", "Convenor"): 50,
        ("National (<1W)", "Internal", "Co-convenor"): 25,
        ("National (<1W)", "Internal", "Sponsor"): 40,
        ("National (<1W)", "Internal", "Internal"): 30,
    }

    return points_dict.get((fdp_type, funding_type, capacity), 0)  # Return 0 if no mapping found

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()

    with st.form("l7"):
        st.title("FDPs Conducted")

        fdp_type_options = ["International (>=2W)", "National (>=2W)", "International (1W to 2W)", "National (1W to 2W)", "International (<1W)", "National (<1W)"]
        fdp_type = st.selectbox("FDP Type", options=fdp_type_options)

        funding_options = ["External", "Sponsor", "Internal"]
        funding_type = st.selectbox("Funding Type", options=funding_options)

        capacity_options = ["Convenor", "Co-convenor", "Sponsor", "Internal"]
        capacity = st.selectbox("Capacity", options=capacity_options)

        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title of Event", value="", placeholder="Enter Event Title")
        with col2:
            ht = st.text_input("Host Institution", value="", placeholder="Enter Host Institution")

        col1, col2, col3 = st.columns(3)
        with col1:
            frod = st.date_input("FDP Started Date", today, format="MM.DD.YYYY")
        with col2:
            tod = st.date_input("FDP Ended Date", today, format="MM.DD.YYYY")
        with col3:
            days = st.text_input("No of Days", value="", placeholder="Enter Event No of Days")

        certificate_file = st.file_uploader("Upload Your FDP Certificate PDF", type=["pdf"])

        # Calculate points based on selected options
        points = get_points(fdp_type, funding_type, capacity)

        # Fetch and display dynamically added inputs
        custom_inputs = get_custom_inputs("l7")
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
            if not title or not ht or not days:
                st.error("Please fill out all required fields.")
                return

            if not certificate_file:
                st.error("Please upload your FDP certificate PDF.")
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
                    "fdp_type": fdp_type,
                    "event_title": pascal_case(title),
                    "host_institution": pascal_case(ht),
                    "start_date": frod.strftime("%Y-%m-%d"),
                    "end_date": tod.strftime("%Y-%m-%d"),
                    "no_of_days": days,
                    "points": points,  # Add points to the data
                    "department": department,
                    "date": datetime.datetime.now(),
                    "certificate_file": encoded_certificate
                }

                # Add custom inputs to the data dictionary
                data.update(additional_data)

                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.subheader("FDPs Conducted This Year")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username", "certificate_file"], errors='ignore')  # Drop unnecessary columns
            st.table(df)
        else:
            st.write("No data found for this year.")

if __name__ == "__main__":
    main(st.session_state.username)
