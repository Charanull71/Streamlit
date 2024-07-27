import streamlit as st
import time
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection_l2 = db['l2']

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

def main(username):
    st.title("Student Project Works Undertaken")

    st.header("B.Tech Project")
    with st.form(key='btech_form'):
        btech_reg_no = st.text_input("B.Tech Student Register No.")
        btech_submitted = st.radio("B.Tech Project Submitted?", ["YES", "NO"])
        btech_grade = st.selectbox("B.Tech Project Grade", ["O", "A+", "A", "B+", "B", "C", "P", "F"])
        btech_published = st.radio("B.Tech Project Research output is published?", ["YES", "NO"])
        btech_submit_button = st.form_submit_button(label="Submit")

        if btech_submit_button:
            if not btech_reg_no:
                st.error("Please fill out all fields.")
            else:
                btech_points = calculate_btech_points(btech_grade)
                st.write(f"B.Tech Project Points: {btech_points}")

                data = {
                    "username": username,
                    "project_type": "B.Tech",
                    "reg_no": btech_reg_no,
                    "submitted": btech_submitted,
                    "grade": btech_grade,
                    "published": btech_published,
                    "points": btech_points,
                    "date": datetime.datetime.now()
                }
                collection_l2.insert_one(data)
                st.success("B.Tech project data inserted successfully!")

    st.header("M.Tech/MBA Project")
    with st.form(key='mtech_form'):
        mtech_reg_no = st.text_input("M.Tech/MBA Student Register No.")
        mtech_program = st.text_input("M.Tech/MBA Program")
        mtech_specialization = st.text_input("M.Tech/MBA Specialisation/Dept")
        mtech_grade = st.selectbox("M.Tech/MBA Project Grade", ["Excellent", "Good", "Satisfactory"])
        mtech_publication = st.selectbox("M.Tech/MBA Project Research output is published in:", ["Scopus & above", "Non Scopus"])
        mtech_submit_button = st.form_submit_button(label="Submit")

        if mtech_submit_button:
            if not (mtech_reg_no and mtech_program and mtech_specialization):
                st.error("Please fill out all fields.")
            else:
                mtech_points = calculate_mtech_points(mtech_grade, mtech_publication)
                st.write(f"M.Tech/MBA Project Points: {mtech_points}")

                data = {
                    "username": username,
                    "project_type": "M.Tech/MBA",
                    "reg_no": mtech_reg_no,
                    "program": mtech_program,
                    "specialization": mtech_specialization,
                    "grade": mtech_grade,
                    "publication": mtech_publication,
                    "points": mtech_points,
                    "date": datetime.datetime.now()
                }
                collection_l2.insert_one(data)
                st.success("M.Tech/MBA project data inserted successfully!")

if __name__ == "__main__":
    main(st.session_state.username)
