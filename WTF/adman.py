import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

def main():
    # MongoDB Connection
    client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
    db = client['Streamlit']
    custom_inputs_collection = db['custom_inputs']

    st.title("Admin Panel: Add & Delete Custom Input Fields")

    # --- Section: Add New Input Field ---
    st.header("Add New Input Field")
    input_name = st.text_input("Input Field Name (e.g., book_feature)")
    input_type = st.selectbox("Input Type", ["Text", "Dropdown", "Media"])

    # Show options for dropdown if input_type is 'Dropdown'
    dropdown_options = ""
    if input_type == "Dropdown":
        dropdown_options = st.text_area("Options for Dropdown (comma-separated)", placeholder="e.g., Option 1, Option 2")

    selected_page = st.selectbox("Select Page", ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9", "l10", "l11", "l12", "l13", "l14", "l15", "l16", "l17", "l18", "l19", "l20", "l21", "l22"])
    selected_role = st.selectbox("Select Role", ["Faculty", "HOD", "Principal"])

    if st.button("Add Input Field"):
        if input_name and input_type and selected_page and selected_role:
            options_list = dropdown_options.split(",") if dropdown_options else []

            input_data = {
                "input_name": input_name,
                "input_type": input_type,
                "options": options_list,
                "page": selected_page,
                "role": selected_role,
                "organisation": st.session_state.organisation
            }
            custom_inputs_collection.insert_one(input_data)
            st.success(f"Input field '{input_name}' added successfully to page '{selected_page}' for role '{selected_role}'.")
            st.rerun()  # Refresh the page after adding a new field
        else:
            st.warning("Please fill in all fields.")

    # --- Section: Delete Existing Custom Input Fields ---
    st.header("Delete Custom Input Fields")

    # Fetch all custom input fields
    custom_inputs = list(custom_inputs_collection.find())

    if not custom_inputs:
        st.write("No custom fields have been added yet.")
    else:
        for custom_input in custom_inputs:
            with st.expander(f"{custom_input['input_name']} - {custom_input['input_type']}"):
                st.write(f"**Input Type:** {custom_input['input_type']}")
                st.write(f"**Page:** {custom_input['page']}")
                st.write(f"**Role:** {custom_input['role']}")
                if custom_input['input_type'] == "Dropdown":
                    st.write(f"**Options:** {', '.join(custom_input['options'])}")

                # Delete button for each field
                if st.button(f"Delete '{custom_input['input_name']}'", key=str(custom_input["_id"])):
                    custom_inputs_collection.delete_one({"_id": ObjectId(custom_input["_id"])})
                    st.success(f"Custom input field '{custom_input['input_name']}' deleted successfully.")
                    st.rerun()  # Refresh the page after deletion

# Call the main function to run the app

