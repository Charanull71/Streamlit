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
    "If student selected for selected for a company other than MNC": 4,
    "If student Promoted/Releived without any of the above": 3,
    "If student Discontined/Detained": 0
}

def main(username):
    with st.form("l9"):
        st.title("Students Counselling/Mentoring")

        year_department = st.text_input("Year & Department", value="", placeholder="Enter Year & Department")
        student_regd_nos = st.text_input("Regd. no(s). of student", value="", placeholder="18A51A0501-18A51A0521")
        number_of_students = st.text_input("Number of students", value="", placeholder="Enter number of students")
        specific_remarks = st.text_input("Specific remarks", value="", placeholder="Enter specific remarks (e.g., 16 Selected in Campus Interviews)")

        # Dropdown for student outcome
        student_outcome = st.selectbox(
            "Select student outcome",
            list(points_dict.keys())
        )

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not year_department or not student_regd_nos or not number_of_students or not specific_remarks or not student_outcome:
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

                # Calculate points based on student outcome and number of students
                points = points_dict[student_outcome] * int(number_of_students)

                data = {
                    "username": username,
                    "year_department": year_department,
                    "student_regd_nos": student_regd_nos,
                    "number_of_students": number_of_students,
                    "specific_remarks": specific_remarks,
                    "student_outcome": student_outcome,
                    "points": points,
                    "department": department,
                    "date": datetime.datetime.now()
                }

                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        st.subheader("Students Counselling(Current Academic Year)")
        start_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
        end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)
        query = {"username": username, "date": {"$gte": start_date, "$lte": end_date}}
        records = list(collection.find(query))

        if records:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "username"])  # Drop columns that are not needed in the table
            st.table(df)
        else:
            st.write("No data found for this year.")
if __name__ == "__main__":
    # Replace 'your_username' with the actual username
    main(st.session_state.username)
