import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l20']
collection_users = db['users']
# Point calculation based on award type
def calculate_points(award_type):
    if award_type == "International":
        return 100
    elif award_type == "National":
        return 50
    elif award_type == "State Level":
        return 25
    elif award_type == "University Level":
        return 15
    else:
        return 0

def main(username):
    # st.set_page_config(page_title="Streamlit Fellowship/Award Form", page_icon=":star2:")

    st.title("FELLOWSHIP/AWARD")

    # total_received_previous = st.text_input("No. Of Fellowship/Awards received upto previous assessment year (in Rs.)", value="", key="total_received_previous")
    # st.text("")

    award_name = st.text_input("Fellowship/Award Name", value="", key="award_name")
    award_type = st.selectbox("Fellowship/Award Type", ("International", "National", "State Level", "University Level"), key="award_type")
    points = calculate_points(award_type)

    if st.button("Submit Award"):
        # Validate and store fellowship/award data in MongoDB
        if not (award_name and award_type):
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
                "username":st.session_state.username,
                "department":department,
                "award_name": award_name,
                "award_type": award_type,
                "points": points,
                "date": datetime.datetime.now()
            }

            collection.insert_one(data)
            st.success("Fellowship/Award data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

if __name__ == "__main__":
    main(st.session_state.username)