import streamlit as st
import datetime
from pymongo import MongoClient
import pandas as pd
from .l1 import pascal_case  # Ensure this import is correct and relevant

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l19']  # Replace 'l19' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def calculate_points(position):
    """
    Function to calculate points based on the position in the project team.
    """
    if position == "Single":
        return 100
    elif position == "First or Principal Person":
        return 50
    elif position == "Other Persons":
        return 10
    else:
        return 0

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    st.title("FUNDED PROJECTS")
    st.subheader("Funded Projects in the Present Assessment Year")

    title = st.text_input("Title of Project", value="", placeholder="Enter Title")
    position = st.selectbox("Position in the Team", ("Single", "First or Principal Person", "Other Persons"))
    funded_by = st.text_input("Funded By", value="", placeholder="Enter Funding Source")

    col1, col2 = st.columns(2)
    with col1:
        period_from = st.date_input("Period From", datetime.date.today())
    with col2:
        period_to = st.date_input("Period To", datetime.date.today())

    grant_amount = st.text_input("Grant/Amount Mobilised", value="", placeholder="Enter Amount")
    pi_option = st.selectbox("Are you PI?", ("Yes", "No"))

    # Fetch and display dynamically added inputs (e.g., media, dropdowns)
    custom_inputs = get_custom_inputs("l19")
    additional_data = {}

    for custom_input in custom_inputs:
        if custom_input['input_type'] == "Text":
            additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
        elif custom_input['input_type'] == "Dropdown":
            additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
        elif custom_input['input_type'] == "Media":
            additional_data[custom_input['input_name']] = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Submit"):
        # Validate and store project data in MongoDB
        points = calculate_points(position)

        if not (title and funded_by and period_from and period_to and grant_amount):
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

            data = {
                "username": username,
                "department": department,
                "title": pascal_case(title),
                "position": position,
                "funded_by": pascal_case(funded_by),
                "period_from": period_from,
                "period_to": period_to,
                "grant_amount": grant_amount,
                "pi_option": pi_option,
                "date": datetime.datetime.now(),
                "points": points  # Include calculated points
            }
            # Add custom inputs to the data dictionary
            data.update(additional_data)

            collection.insert_one(data)
            st.success("Project data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.subheader("Projects Funded This Year")
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
