import streamlit as st
from pymongo import MongoClient
import datetime
from datetime import date

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection_l3 = db['l3']

def calculate_training_points(activity_type, hours):
    activity_points = {
        "Modular Program/Technical training [coordinator]": 100,
        "Resource person": 50,
        "Bridge course/remedial/makeup": 50,
        "Tutorial classes": 20
    }
    return activity_points.get(activity_type, 0) * hours

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
        year_program = st.text_input("Year & Program")
        dept_specialization = st.text_input("Dept./Specialisation")
        period_from = st.date_input("From", value=date.today())
        period_to = st.date_input("To", value=date.today())
        hours = st.number_input("Hours", min_value=0, step=1)
        description = st.text_area("Brief description of program")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if not (activity_type and year_program and dept_specialization and hours and description):
                st.error("Please fill out all fields.")
            else:
                training_points = calculate_training_points(activity_type, hours)
                st.write(f"Training Activity Points: {training_points}")

                data = {
                    "username": username,
                    "activity_type": activity_type,
                    "year_program": year_program,
                    "dept_specialization": dept_specialization,
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

if __name__ == "__main__":
    main(st.session_state.username)
