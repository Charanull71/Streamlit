import streamlit as st
import datetime
from pymongo import MongoClient
import base64
import pandas as pd
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l6']  # Replace 'l6' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

def get_points(level_of_institute, duration):
    """
    Function to get the points based on the level of institute and duration of the FDP.
    """
    if level_of_institute == "IIT":
        if duration == ">=2W":
            return 100
        elif duration == "1W-2W":
            return 90
        elif duration == "<1W":
            return 80
    elif level_of_institute == "NIT":
        if duration == ">=2W":
            return 90
        elif duration == "1W-2W":
            return 80
        elif duration == "<1W":
            return 70
    elif level_of_institute == "University":
        if duration == ">=2W":
            return 80
        elif duration == "1W-2W":
            return 70
        elif duration == "<1W":
            return 60
    elif level_of_institute == "College":
        if duration == ">=2W":
            return 70
        elif duration == "1W-2W":
            return 60
        elif duration == "<1W":
            return 50
    return 0

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()

    with st.form("l6"):
        st.title("FDPs Attended")
        
        Subject = st.text_input("Name of the FDP", value="", placeholder="Enter FDP Name")
        
        level_options = ["IIT", "NIT", "University", "College"]
        level_of_institute = st.selectbox(
            "Level of Institute",
            options=level_options,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        col1,col2 =st.columns(2)
        with col1:
            title = st.text_input("Title of Event", value="", placeholder="Enter Event Title")
        with col2:
            ht = st.text_input("Host Institution", value="", placeholder="Enter Host Institution")
        col1,col2,col3 =st.columns(3)
        with col1:
            frod = st.date_input("FDP Started Date", today, format="MM.DD.YYYY")
        with col2:
            tod = st.date_input("FDP Ended Date", today, format="MM.DD.YYYY")
        with col3:
            days = st.text_input("No of Days", value="", placeholder="Enter Event No of Days")
        
        duration_options = [">=2W", "1W-2W", "<1W"]
        fdp_duration = st.selectbox(
            "Duration of the FDP",
            options=duration_options,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        
        certificate_file = st.file_uploader("Upload Your FDP Certificate PDF", type=["pdf"])

        # Calculate points based on selected options
        points = get_points(level_of_institute, fdp_duration)



        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject or not title or not ht or not days:
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
                    "fdp_name": Subject,
                    "institute_level": level_of_institute,
                    "event_title": title,
                    "host_institution": ht,
                    "start_date": frod.strftime("%Y-%m-%d"),
                    "end_date": tod.strftime("%Y-%m-%d"),
                    "no_of_days": days,
                    "fdp_duration": fdp_duration,
                    "points": points,  # Add points to the data
                    "department": department,
                    "date": datetime.datetime.now(),
                    "certificate_file": encoded_certificate
                }

                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        st.subheader("FDPs Attended This Year")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username","certificate_file"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")
if __name__ == "__main__":
    # Ensure the username is set in session state before running the main function
  # Replace 'your_username' with the actual username
    main(st.session_state.username)
