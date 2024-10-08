import streamlit as st
import datetime
from pymongo import MongoClient
import pandas as pd
from .l1 import pascal_case

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection_l2_btech = db['l2_btech']
collection_l2_mtech = db['l2_mtech']
custom_inputs_collection = db['custom_inputs']  # Collection for dynamic custom fields

# Grade points for B.Tech and M.Tech
def calculate_btech_points(grade):
    grade_points = {
        "O": 100,
        "A+": 90,
        "A": 80,
        "B+": 70,
        "B": 60,
        "C": 50,
        "P": 40,
        "F": 0
    }
    return grade_points.get(grade, 0)

def calculate_mtech_points(grade, publication):
    grade_points = {
        ("Excellent", "Scopus & above"): 100,
        ("Excellent", "Non Scopus"): 80,
        ("Good", "Scopus & above"): 90,
        ("Good", "Non Scopus"): 70,
        ("Satisfactory", "Scopus & above"): 80,
        ("Satisfactory", "Non Scopus"): 60
    }
    return grade_points.get((grade, publication), 0)

def get_dynamic_fields(project_type):
    """Fetch dynamic fields from custom_inputs collection based on project type and role"""
    query = {
        "page": "l2",  # Assuming 'l2' is the page identifier for project works
        "project_type": project_type,
        "role": "Faculty"  # Modify this if roles vary
    }
    custom_fields = list(custom_inputs_collection.find(query))
    return custom_fields

def render_dynamic_fields(custom_fields):
    """Render dynamic form fields based on custom_fields configuration"""
    dynamic_data = {}
    for field in custom_fields:
        field_name = field["input_name"]
        field_type = field["input_type"]
        
        if field_type == "Text":
            dynamic_data[field_name] = st.text_input(f"{field_name}")
        elif field_type == "Dropdown":
            dynamic_data[field_name] = st.selectbox(f"{field_name}", field["options"])
        elif field_type == "Media":
            dynamic_data[field_name] = st.file_uploader(f"{field_name}")
    return dynamic_data

def main(username):
    st.title("Student Project Works Undertaken")

    # Dropdown to select project type
    if 'project_type' not in st.session_state:
        st.session_state.project_type = "B.Tech"  # Default value

    # Project type selection
    project_type = st.selectbox("Select Project Type", ["B.Tech", "M.Tech/MBA"], index=["B.Tech", "M.Tech/MBA"].index(st.session_state.project_type))

    # Update session state with the selected project type
    if project_type != st.session_state.project_type:
        st.session_state.project_type = project_type
        st.rerun()

    # Fetch dynamic fields for the selected project type
    custom_fields = get_dynamic_fields(st.session_state.project_type)

    if st.session_state.project_type == "B.Tech":
        st.header("B.Tech Projects")
        with st.form(key='btech_form'):
            btech_reg_no = st.text_input("B.Tech Student Register No.")
            btech_submitted = st.radio("B.Tech Project Submitted?", ["YES", "NO"])
            btech_grade = st.selectbox("B.Tech Project Grade", ["O", "A+", "A", "B+", "B", "C", "P", "F"])
            btech_published = st.radio("B.Tech Project Research output is published?", ["YES", "NO"])

            # Render dynamic fields for B.Tech
            dynamic_data = render_dynamic_fields(custom_fields)

            btech_submit_button = st.form_submit_button(label="Submit B.Tech Project")
            if btech_submit_button:
                if not btech_reg_no:
                    st.error("Please fill out all fields.")
                else:
                    btech_points = calculate_btech_points(btech_grade)
                    # Combine static and dynamic data
                    data = {
                        "username": username,
                        "project_type": "B.Tech",
                        "reg_no": pascal_case(btech_reg_no),
                        "submitted": btech_submitted,
                        "grade": btech_grade,
                        "published": btech_published,
                        "points": btech_points,
                        "date": datetime.datetime.now()
                    }
                    data.update(dynamic_data)  # Add dynamic fields data
                    collection_l2_btech.insert_one(data)
                    st.success("B.Tech project data inserted successfully!")

        # Show existing records
        st.subheader("Student Project Works Undertaken This Year(B.Tech)")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection_l2_btech.find(query))
        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")

    elif st.session_state.project_type == "M.Tech/MBA":
        st.header("M.Tech/MBA Projects")
        with st.form(key='mtech_form'):
            mtech_reg_no = st.text_input("M.Tech/MBA Student Register No.")
            mtech_program = st.selectbox("M.Tech/MBA Program", ["M.Tech", "MBA"])
            mtech_specialization = st.text_input("M.Tech/MBA Specialisation/Dept")
            mtech_grade = st.selectbox("M.Tech/MBA Project Grade", ["Excellent", "Good", "Satisfactory"])
            mtech_publication = st.selectbox("M.Tech/MBA Project Research output is published in:", ["Scopus & above", "Non Scopus"])

            # Render dynamic fields for M.Tech/MBA
            dynamic_data = render_dynamic_fields(custom_fields)

            mtech_submit_button = st.form_submit_button(label="Submit M.Tech/MBA Project")
            if mtech_submit_button:
                if not (mtech_reg_no and mtech_specialization):
                    st.error("Please fill out all fields.")
                else:
                    mtech_points = calculate_mtech_points(mtech_grade, mtech_publication)
                    # Combine static and dynamic data
                    data = {
                        "username": username,
                        "project_type": "M.Tech/MBA",
                        "reg_no": mtech_reg_no,
                        "program": mtech_program,
                        "specialization": pascal_case(mtech_specialization),
                        "grade": mtech_grade,
                        "publication": mtech_publication,
                        "points": mtech_points,
                        "date": datetime.datetime.now()
                    }
                    data.update(dynamic_data)  # Add dynamic fields data
                    collection_l2_mtech.insert_one(data)
                    st.success("M.Tech/MBA project data inserted successfully!")

        # Show existing records
        st.subheader("Student Project Works Undertaken This Year(M.Tech/MBA)")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection_l2_mtech.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")

if __name__ == "__main__":
    if 'username' in st.session_state:
        main(st.session_state.username)
    else:
        st.warning("Please log in first.")
