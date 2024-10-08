import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l17']  # Replace 'l17' with your actual collection name
collection_users = db['users']  # Replace with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

# Define points for each position in the team
def calculate_points(position):
    POSITION_POINTS = {
        "Single": 100,
        "First or Principal person": 50,
        "Other Persons": 10
    }
    return POSITION_POINTS.get(position, 0)

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    with st.form("l17"):
        st.title("PRODUCT DESIGN / SOFTWARE DEVELOPMENT")

        # Previous assessment year products
        n1 = st.text_input("No. Of Products designed/developed up to previous assessment year:")

        # Current assessment year products
        st.write("No. Of Products designed/developed in present assessment year:")
        col1, col2 = st.columns(2)
        with col1:
            nop = st.text_input("Name of Product / SW", value="", placeholder="Enter Name of Product / SW")
        with col2:
            nof = st.text_input("No. Of Faculty in the team work", value="", placeholder="Enter No. Of Faculty in the team work")

        pos = st.selectbox("Position in the team", options=["Single", "First or Principal person", "Other Persons"])
        pos_points = calculate_points(pos)

        dop = st.text_input("Description of the product / SW", value="", placeholder="Enter Description of the product / SW")

        # Fetch and display dynamically added inputs
        custom_inputs = get_custom_inputs("l17")
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
            if not (n1 and nop and nof and dop):
                st.error("Please fill out all required fields.")
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
                    "products_previous": n1,
                    "product_name": nop,
                    "faculty_count": nof,
                    "position_in_team": pos,
                    "position_points": pos_points,
                    "product_description": dop,
                    "department": department,
                    "date": datetime.datetime.now()
                }

                # Add custom inputs to the data dictionary
                data.update(additional_data)

                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.subheader("Products Developed This Year")
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
