import streamlit as st
from pymongo import MongoClient
import datetime
from datetime import date
import pandas as pd
from .l1 import pascal_case
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection_l3 = db['l3']
collection_users = db['users']
def calculate_training_points(activity_type, hours):
    activity_points = {
        "Modular Program/Technical training [coordinator]": 100,
        "Resource person": 50,
        "Bridge course/remedial/makeup": 50,
        "Tutorial classes": 20
    }
    return activity_points.get(activity_type, 0)

def main(username):
    st.title("Student Training Activities")

    st.header("Training Activity Details")
    with st.form(key='training_form'):
        activity_type = st.selectbox("Type of Activity", [
            "Modular Program/Technical training [coordinator]", 
            "Resource person", 
            "Bridge course/remedial/makeup", 
            "Tutorial classes"
        ])
        col1, col2,col3 = st.columns(3)
        with col1:
            year=  st.selectbox(
        "Year",
        ("1", "2", "3","4"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
        with col2:
            program = st.text_input("Program")
        with col3:
            dept = st.selectbox(
        "Department",
        ("CSE", "CSM", "CSD","ECE","EEE","IT","MECH","CIVIL"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

        col1,col2,col3=st.columns(3)
        with col1:
            period_from = st.date_input("From", value=date.today())
        with col2:
            period_to = st.date_input("To", value=date.today())
        with col3:
            hours = st.number_input("Hours", min_value=0, step=1)
        description = st.text_area("Brief description of program")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if not (activity_type and year and program and dept and hours and description):
                st.error("Please fill out all fields.")
            else:
                training_points = calculate_training_points(activity_type, hours)
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return

                data = {
                    "username": username,
                    "activity_type": activity_type,
                    "year_program": year+" "+pascal_case(program),
                    "dept_specialization": dept,
                    "period_from": datetime.datetime.combine(period_from, datetime.datetime.min.time()),
                    "period_to": datetime.datetime.combine(period_to, datetime.datetime.min.time()),
                    "hours": hours,
                    "description": description,
                    "points": training_points,
                    "date": datetime.datetime.now()
                }
                try:
                    collection_l3.insert_one(data)
                    st.success("Training activity data inserted successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    st.subheader("Training Activities This Year")
    start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
    end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
    query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
    records = list(collection_l3.find(query))

    if records:
        df = pd.DataFrame(records)
        df = df.drop(columns=["_id", "username"])  # Drop columns that are not needed in the table
        st.table(df)
    else:
        st.write("No data found for this year.")
if __name__ == "__main__":
    main(st.session_state.username)
