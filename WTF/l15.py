import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l15']  # Replace 'l15' with your actual collection name for book publications
collection_users = db['users']  # Replace 'users' with your actual collection name for users
collection_custom = db['custom_inputs']  # Collection for dynamic inputs

def calculate_book_points(issn_isbn, position_of_authorship, publishing_house_level):
    is_international = "International" in publishing_house_level
    has_isbn = issn_isbn.strip().upper() == "YES"
    is_first_author = "1st" in position_of_authorship.lower()

    if is_international:
        if has_isbn:
            return 100 if is_first_author else 25
        else:
            return 50 if is_first_author else 10
    else:
        if has_isbn:
            return 75 if is_first_author else 10
        else:
            return 35 if is_first_author else 5

def get_custom_inputs(page):
    return list(collection_custom.find({"page": page}))

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    with st.form("l15"):
        st.title("BOOK PUBLICATIONS")

        n1 = st.text_input("No. Of Books Published up to the previous assessment year:")
        st.write("Books Published in present assessment year:")
        aut = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pos = st.selectbox("Position of authorship", ["1st author", "Co-author", "Other author"])
        iss = st.selectbox("ISSN/ISBN No.", ["", "YES", "NO"])
        lph = st.selectbox("Level of Publishing House", ["International Publisher", "National Publisher"])
        tpb = st.text_input("Title and other particulars of the book", value="", placeholder="Enter Title and other particulars of the book")

        # Fetch and display dynamically added inputs (e.g., media, dropdowns)
        custom_inputs = get_custom_inputs("l15")
        additional_data = {}

        for custom_input in custom_inputs:
            if custom_input['input_type'] == "Text":
                additional_data[custom_input['input_name']] = st.text_input(custom_input['input_name'])
            elif custom_input['input_type'] == "Dropdown":
                additional_data[custom_input['input_name']] = st.selectbox(custom_input['input_name'], custom_input['options'])
            elif custom_input['input_type'] == "Media":
                additional_data[custom_input['input_name']] = st.file_uploader(f"Upload {custom_input['input_name']} (Media)", type=["jpg", "jpeg", "png", "pdf"])

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and aut and pos and iss and lph and tpb):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                # Calculate points
                points = calculate_book_points(iss, pos, lph)

                data = {
                    "username": username,
                    "books_published_previous": n1,
                    "authors": aut,
                    "position_of_authorship": pos,
                    "issn_isbn": iss,
                    "publishing_house_level": lph,
                    "book_particulars": tpb,
                    "department": department,
                    "points": points,
                    "date": datetime.datetime.now()
                }

                # Add custom inputs to the data dictionary
                data.update(additional_data)

                collection.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.subheader("Book Publications This Year")
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
