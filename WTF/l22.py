import streamlit as st
import datetime
from pymongo import MongoClient
from .l1 import pascal_case  # Ensure this import is correct and relevant

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l22']  # Adjusted to use 'l22' collection
collection_users = db['users']  # Users collection
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    st.title("LEAVES AVAILED")

    # Date dropdowns for 'From' and 'To' dates
    col1, col2 = st.columns(2)
    with col1:
        from_date = st.date_input("From Date", datetime.datetime.now())
    with col2:
        to_date = st.date_input("To Date", datetime.datetime.now())

    # Standard leave fields
    classes = st.number_input("Cls", min_value=0, step=1, value=0, key="classes")
    hp_classes = st.number_input("HP Cls", min_value=0, step=1, value=0, key="hp_classes")
    c_classes = st.number_input("C Cls", min_value=0, step=1, value=0, key="c_classes")
    ods = st.number_input("ODs", min_value=0, step=1, value=0, key="ods")
    study_leaves = st.number_input("Study leaves", min_value=0, step=1, value=0, key="study_leaves")
    academic_leaves = st.number_input("Academic leaves", min_value=0, step=1, value=0, key="academic_leaves")
    permissions = st.number_input("No. of permissions", min_value=0, step=1, value=0, key="permissions")
    other_leaves_remarks = st.text_area("Any other leaves & remarks", "", key="other_leaves_remarks")

    # Fetch and display dynamically added inputs (if any)
    custom_inputs = get_custom_inputs("l22")  # Fetching dynamic inputs for page 'l22'
    additional_data = {}

    for custom_input in custom_inputs:
        if custom_input['input_type'] == "Text":
            additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
        elif custom_input['input_type'] == "Dropdown":
            additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
        elif custom_input['input_type'] == "Media":
            additional_data[custom_input['input_name']] = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Submit"):
        # Validate and store leaves availed details in MongoDB
        try:
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return

            # Prepare data for insertion
            data = {
                "username": username,
                "department": department,
                "from_date": from_date.strftime('%Y-%m-%d') if isinstance(from_date, datetime.date) else None,
                "to_date": to_date.strftime('%Y-%m-%d') if isinstance(to_date, datetime.date) else None,
                "classes": classes,
                "hp_classes": hp_classes,
                "c_classes": c_classes,
                "ods": ods,
                "study_leaves": study_leaves,
                "academic_leaves": academic_leaves,
                "permissions": permissions,
                "other_leaves_remarks": pascal_case(other_leaves_remarks),
                "date": datetime.datetime.now()
            }

            # Add custom inputs to the data dictionary
            data.update(additional_data)

            # Insert into MongoDB
            collection.insert_one(data)
            st.success("Leaves availed data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
