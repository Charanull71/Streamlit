import streamlit as st
import datetime
from pymongo import MongoClient
import pandas as pd
from .l1 import pascal_case
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l19']
collection_users = db['users']
def calculate_points(position):
    if position == "Single":
        return 100
    elif position == "First or Principal Person":
        return 50
    elif position == "Other Persons":
        return 10
    else:
        return 0
def main(username):
    st.title("FUNDED PROJECTS")
    st.subheader("Funded Projects in the present assessment year")
    title = st.text_input("Title of Project", value="", placeholder="Enter Title")
    position = st.selectbox("Position in the team", ("Single", "First or Principal Person", "Other Persons"))
    funded_by = st.text_input("Funded by", value="", placeholder="Enter Funding Source")
    col1,col2 =st.columns(2)
    with col1:
        period_from = st.date_input("Period From")
    with col2:
        period_to = st.date_input("Period To")
    grant_amount = st.text_input("Grant/Amount Mobilised", value="", placeholder="Enter Amount")
    pi_option = st.selectbox("Are you PI?", ("Yes", "No"))
    

    if st.button("Submit"):
        # Validate and store project data in MongoDB
        points = calculate_points(position)
        if not (title and funded_by and period_from and period_to and grant_amount):
            st.error("Please fill out all fields.")
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
            data = {
                "username":username,
                "department":department,
                "title": pascal_case(title),
                "position":position,
                "funded_by": pascal_case(funded_by),
                "period_from": period_from,
                "period_to": period_to,
                "grant_amount": grant_amount,
                "pi_option": pi_option,
                "date": datetime.datetime.now()
            }
            collection.insert_one(data)
            st.success("Project data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    st.subheader("Projects Funded This Year")
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
    main(st.session_state.username)