import streamlit as st
import datetime
from pymongo import MongoClient
import pandas as pd
from .l1 import pascal_case  # Ensure this import is correct

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l20']  # Collection for fellowship/awards
collection_users = db['users']  # Users collection
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

# Point calculation based on award type
def calculate_points(award_type):
    if award_type == "International":
        return 100
    elif award_type == "National":
        return 50
    elif award_type == "State Level":
        return 25
    elif award_type == "University Level":
        return 15
    else:
        return 0

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    st.title("FELLOWSHIP/AWARD")

    award_name = st.text_input("Fellowship/Award Name", value="", key="award_name")
    award_type = st.selectbox("Fellowship/Award Type", 
                               ("International", "National", "State Level", "University Level"), 
                               key="award_type")
    
    # Calculate points based on the selected award type
    points = calculate_points(award_type)

    # Fetch and display dynamically added inputs
    custom_inputs = get_custom_inputs("l20")
    additional_data = {}

    for custom_input in custom_inputs:
        if custom_input['input_type'] == "Text":
            additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
        elif custom_input['input_type'] == "Dropdown":
            additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
        elif custom_input['input_type'] == "Media":
            additional_data[custom_input['input_name']] = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", 
                                                                             type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Submit Award"):
        # Validate and store fellowship/award data in MongoDB
        if not (award_name and award_type):
            st.error("Please fill out all fields.")
            return

        try:
            # Query users collection to get department for the specified username
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return
            
            # Prepare the data for insertion
            data = {
                "username": username,
                "department": department,
                "award_name": pascal_case(award_name),
                "award_type": award_type,
                "points": points,
                "date": datetime.datetime.now()
            }

            # Add custom inputs to the data dictionary
            data.update(additional_data)

            # Insert the data into the collection
            collection.insert_one(data)
            st.success("Fellowship/Award data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

    # Display submitted awards/fellowships for the current academic year
    st.subheader("Awards/Fellowships (Current Academic Year)")
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
