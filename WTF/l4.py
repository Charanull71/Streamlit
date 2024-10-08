import streamlit as st
import time
from pymongo import MongoClient
import datetime
import pandas as pd
from .l1 import pascal_case

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l4']  # Replace 'l4' with your actual collection name
custom_inputs_collection = db['custom_inputs']  # Collection to fetch admin-added fields

def get_points(material_type, involvement_type):
    """
    Function to get the points based on the type of material and type of involvement.
    """
    if material_type == "ICT Based teaching Material":
        if involvement_type == "Single":
            return 100
        elif involvement_type == "More than one":
            return 50
    elif material_type == "Interactive Courses/Online Courses":
        if involvement_type == "Single":
            return 75
        elif involvement_type == "More than one":
            return 35
    elif material_type == "Participatory Learning Modules/Teaching Notes":
        if involvement_type == "Single":
            return 50
        elif involvement_type == "More than one":
            return 25
    return 0

def load_custom_fields(page_name, role):
    """Fetch and return custom input fields for the specified page and role."""
    query = {"page": page_name, "role": role}
    return list(custom_inputs_collection.find(query))

def render_custom_fields(custom_fields):
    """Dynamically render custom fields based on admin configuration."""
    custom_data = {}
    for field in custom_fields:
        field_name = field['input_name']
        input_type = field['input_type']
        
        if input_type == "Text":
            custom_data[field_name] = st.text_input(f"{field_name}")
        elif input_type == "Dropdown":
            options = field.get('options', [])
            custom_data[field_name] = st.selectbox(f"{field_name}", options)
        elif input_type == "Media":
            custom_data[field_name] = st.file_uploader(f"{field_name}")
    
    return custom_data

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # Reset session state
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

    st.title("Learning Material")

    Subject = st.text_input(
        "Material Developed for Subject",
        value="",
        placeholder="Enter Your Subject"
    )
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox(
            "Year",
            ("1", "2", "3", "4"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
    with col2:
        dep = st.selectbox(
            "Department",
            ("CSE", "CSM", "CSD", "ECE", "EEE", "IT", "MECH", "CIVIL"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
    col1, col2 = st.columns(2)

    material_options = [
        "ICT Based teaching Material",
        "Interactive Courses/Online Courses",
        "Participatory Learning Modules/Teaching Notes"
    ]
    with col1:
        typem = st.selectbox(
            "Type of Material Developed",
            options=material_options,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
    with col2:
        involvement_options = ["Single", "More than one"]

        option1 = st.selectbox(
            "Type of Involvement",
            options=involvement_options,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    points = get_points(typem, option1)

    # Fetch and render custom fields added by admin
    custom_fields = load_custom_fields("l4", "Faculty")
    custom_field_data = render_custom_fields(custom_fields)  # Render and capture input data

    if st.button("Submit"):
        # Check for empty fields
        if not (Subject and year and dep and typem):
            st.error("Please fill out all fields.")
            return

        try:
            # Collect the dynamic input fields into the submission data
            data = {
                "username": username,
                "subject": pascal_case(Subject),
                "year": year,
                "department": dep,
                "type_of_involvement": option1,
                "type_of_material": typem,
                "points": points,  # Add points to the data
                "date": datetime.datetime.now(),
                **custom_field_data  # Merge custom field data into submission
            }
            collection.insert_one(data)
            st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.subheader("Learning Material Developed This Year")
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
    # Replace 'your_username' with the actual username
    main(st.session_state.username)
