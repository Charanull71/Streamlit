import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l21']
collection_users = db['users']
def main(username):
    # st.set_page_config(page_title="Streamlit Ph.D. Details Form", page_icon="🎓")

    st.title("Ph.D. Details")
    st.subheader("Please fill out the following details:")

    phd_holder = st.radio("Are you a Ph.D. holder?", ("YES", "NO"), index=1)
    
    if phd_holder == "NO":
        year_of_registration = st.number_input("Year of registration for pursuing Ph.D.", min_value=1900, max_value=datetime.datetime.now().year, step=1, value=datetime.datetime.now().year)
    else:
        year_of_registration = None

    course_files_submitted = st.radio("Have you submitted 'Course files of all subjects' up to current month?", ("YES", "NO"))

    if course_files_submitted == "NO":
        reason_files_not_submitted = st.text_area("Reason for not submitting Course files of all subjects", "")

    course_attainment_completed = st.radio("Have you completed 'Course attainment' of all subjects up to current month?", ("YES", "NO"))

    if course_attainment_completed == "NO":
        reason_course_attainment_not_completed = st.text_area("Reason for not completing Course attainment of all subjects", "")

    if st.button("Submit"):
        # Validate and store Ph.D. details in MongoDB
        try:
            username = st.session_state.username  # Replace with your actual way of getting username

                # Query users collection to get department for the specified username
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return
            data = {
                "username":st.session_state.username,
                "department":department,
                "phd_holder": phd_holder,
                "year_of_registration": year_of_registration,
                "course_files_submitted": course_files_submitted,
                "reason_files_not_submitted": reason_files_not_submitted if course_files_submitted == "NO" else None,
                "course_attainment_completed": course_attainment_completed,
                "reason_course_attainment_not_completed": reason_course_attainment_not_completed if course_attainment_completed == "NO" else None,
                "date": datetime.datetime.now()
            }

            collection.insert_one(data)
            st.success("Ph.D. details inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

if __name__ == "__main__":
    main(st.session_state.username)