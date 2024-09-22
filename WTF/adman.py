#ui from admin
import streamlit as st
from pymongo import MongoClient
def main():
    client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
    db = client['Streamlit']
    st.header("Add New Input Field")

    # Input for new field details
    input_name = st.text_input("Input Field Name (e.g., book_feature)")
    input_type = st.selectbox("Input Type", ["Text", "Dropdown", "Media"])
    
    dropdown_options = ""
    if input_type == "Dropdown":
        dropdown_options = st.text_area("Options for Dropdown (comma-separated)", placeholder="e.g., Option 1, Option 2")

    selected_page = st.selectbox("Select Page", ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9", "l10", "l11", "l12", "l13", "l14", "l15", "l16", "l17", "l18", "l19", "l20", "l21", "l22"])
    selected_role = st.selectbox("Select Role", ["Faculty", "HOD", "Principal"])

    if st.button("Submit"):
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
            db['custom_inputs'].insert_one(input_data)
            st.success(f"Input field '{input_name}' added successfully to page '{selected_page}' for role '{selected_role}'.")
        else:
            st.warning("Please fill in all fields.")