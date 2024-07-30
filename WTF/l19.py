import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l19']

def main(username):
    

    st.title("FUNDED PROJECTS")
    st.subheader("Funded Projects in the present assessment year")
    #num_projects = st.number_input("Number of Projects", value=0, min_value=0, max_value=10, step=1)

    
    title = st.text_input("Title of Project", value="", placeholder="Enter Title")
    funded_by = st.text_input("Funded by", value="", placeholder="Enter Funding Source")
    period_from = st.date_input("Period From")
    period_to = st.date_input("Period To")
    grant_amount = st.text_input("Grant/Amount Mobilised", value="", placeholder="Enter Amount")
    pi_option = st.selectbox("Are you PI?", ("Yes", "No"))
       

    if st.button("Submit"):
        # Validate and store project data in MongoDB
        if not (title and funded_by and period_from and period_to and grant_amount):
            st.error("Please fill out all fields.")
            return

        try:
            data = {
                "username":username,
                "title": title,
                "funded_by": funded_by,
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

if __name__ == "__main__":
    main(st.session_state.username)