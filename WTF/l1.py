import streamlit as st
import pandas as pd
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l1']
collection_users = db['users']
collection_custom = db['custom_inputs']
def calpoints(option1, option2, res):
    # Logic to calculate points based on feedback and result percentage
    if option1 == "Excellent" and option2 == "Excellent":
        if int(res) >= 90:
            return 100
        elif int(res) >= 80:
            return 90
        elif int(res) >= 70:
            return 80
        else:
            return 70
    elif option1 == "Good" and option2 == "Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option2 == "Good" and option1 == "Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option1 == "Satisfactory" and option2 == "Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option2 == "Satisfactory" and option1 == "Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1 == "Good" and option2 == "Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option2 == "Good" and option1 == "Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option1 == "Good" and option2 == "Good":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1 == "Satisfactory" and option2 == "Satisfactory":
        if int(res) >= 90:
            return 80
        elif int(res) >= 80:
            return 70
        elif int(res) >= 70:
            return 60
        else:
            return 50

def pascal_case(text):
    # Convert the input text to Pascal Case
    return ' '.join(word.capitalize() for word in text.split())

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    st.title("Theory Courses Handled")

    # Static fields
    Subject = st.text_input("Subject", placeholder="Enter Your Subject")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox("Year", ("1", "2", "3", "4"))
    with col2:
        dep = st.selectbox("Department", ("CSE", "CSM", "CSD", "ECE", "EEE", "IT", "MECH", "CIVIL"))
    with col3:
        section = st.selectbox("Section", ("A", "B", "C", "D", "E", "F"))
    
    col4, col5 = st.columns(2)
    with col4:
        cp = st.text_input("Classes Planned", placeholder="No. Of Classes Planned")
    with col5:
        ch = st.text_input("Classes Held", placeholder="No. Of Classes Held")
    
    col6, col7 = st.columns(2)
    with col6:
        option1 = st.selectbox("Student Feedback (Cycle 1)", ("Excellent", "Good", "Satisfactory"))
    with col7:
        option2 = st.selectbox("Student Feedback (Cycle 2)", ("Excellent", "Good", "Satisfactory"))

    res = st.text_input("Result Of Students", placeholder="% Of Students Passed")

    # Fetch and display dynamically added inputs (e.g., media, dropdowns)
    custom_inputs = get_custom_inputs("l1")
    media_data = None
    additional_data = {}
    
    for custom_input in custom_inputs:
        if custom_input['input_type'] == "Text":
            additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
        elif custom_input['input_type'] == "Dropdown":
            additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
        elif custom_input['input_type'] == "Media":
            media_data = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Submit"):
        if not (Subject and dep and section and cp and ch and res):
            st.error("Please fill out all fields.")
            return

        try:
            points = calpoints(option1, option2, res)
            data = {
                "username": username,
                "subject": pascal_case(Subject),
                "department": dep,
                "section": f"{year} {dep} {section}",
                "classes_planned": cp,
                "classes_held": ch,
                "feedback1": option1,
                "feedback2": option2,
                "result": res,
                "points": points,
                "date": datetime.datetime.now()
            }
            
            # Add custom inputs to the data dictionary
            data.update(additional_data)
            
            # Add media data if available
            if media_data:
                data["media"] = media_data.read()
            
            collection.insert_one(data)
            st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Display data
    st.subheader("Courses Handled This Year")
    start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
    end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
    query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
    records = list(collection.find(query))

    if records:
        df = pd.DataFrame(records)
        df = df.drop(columns=["_id", "username", "media"], errors='ignore')  # Drop unnecessary columns
        st.table(df)
    else:
        st.write("No data found for this year.")

if __name__ == "__main__":
    main(st.session_state.username)
