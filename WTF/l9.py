import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l9']  # Replace 'l9' with your actual collection name
collection_users = db['users']  # Users collection

# Points dictionary for various student outcomes
points_dict = {
    "If student selected for MNC or GATE/GRE qualified or became entrepreneur or got Govt. Job": 5,
    "If student selected for a company other than MNC": 4,
    "If student Promoted/Relieved without any of the above": 3,
    "If student Discontinued/Detained": 0
}

# Predefined B.Tech years as numbers
def get_btech_years():
    return ["1", "2", "3", "4"]

# Predefined departments (or you can fetch dynamically from MongoDB if required)
def get_departments():
    departments = ["CSE", "CSM", "CSD", "ECE", "EEE", "IT", "MECH", "CIVIL"]  # Add more departments as needed
    return departments

def main(username):
    with st.form("l9"):
        st.title("Students Counselling/Mentoring")

        # Dropdown for B.Tech year (numeric)
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("Select Year", get_btech_years())

        # Dropdown for Department
        with col2:
            department = st.selectbox("Select Department", get_departments())

        # Combine Year and Department into a single field for storage
        year_department = f"{year} - {department}"

        # Input for student registration numbers and specific remarks
        student_regd_nos = st.text_input("Regd. no(s). of student", value="", placeholder="18A51A0501-18A51A0521")
        specific_remarks = st.text_input("Specific remarks", value="", placeholder="Enter specific remarks (e.g., 16 Selected in Campus Interviews)")

        # Input for the number of students in each outcome category
        st.write("### Enter the number of students for each outcome:")
        outcomes_data = {}
        total_points = 0
        for outcome, points_per_student in points_dict.items():
            num_students = st.number_input(f"Number of students for: {outcome}", min_value=0, step=1, key=outcome)
            outcomes_data[outcome] = num_students
            total_points += num_students * points_per_student

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not student_regd_nos or not specific_remarks:
                st.error("Please fill out all required fields.")
                return

            try:
                username = st.session_state.username  # Replace with your actual way of getting username

                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return

                # Prepare the data to be inserted into MongoDB
                data = {
                    "username": username,
                    "year_department": year_department,
                    "student_regd_nos": student_regd_nos,
                    "specific_remarks": specific_remarks,
                    "outcomes_data": outcomes_data,
                    "total_points": total_points,
                    "department": department,
                    "date": datetime.datetime.now()
                }

                # Insert the data into MongoDB
                collection.insert_one(data)
                st.success(f"Data inserted successfully with a total of {total_points} points!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Display records from MongoDB for the current academic year
        st.subheader("Students Counselling (Current Academic Year)")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)

            # Exclude 'outcomes_data' column from the table
            df = df.drop(columns=["_id", "username", "outcomes_data"])  # Drop unwanted columns
            st.table(df)
        else:
            st.write("No data found for this year.")

if __name__ == "__main__":
    main(st.session_state.username)
