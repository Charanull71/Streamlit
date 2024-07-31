import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name

# Collections with file fields and their respective fields
collections_with_files = {
    "l5": ["certificate_file"],
    "l6": ["certificate_file"],
    "l8": ["certificate_file"],
    "l10": ["certificate_file"],
    "l11": ["file_uploader"],
    "l12": ["pdf_uploader1", "pdf_uploader2"],
    "l13": ["pdf_uploader"]
}

def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())

def retrieve_data_from_collection(username, collection_name, start_date=None, end_date=None, file_fields=None):
    collection = db[collection_name]
    query = {"username": username}
    
    # Apply date filter to query    
    if start_date and end_date:
        start_datetime = date_to_datetime(start_date)
        end_datetime = date_to_datetime(end_date)
        query["timestamp"] = {"$gte": start_datetime, "$lte": end_datetime}
    
    projection = {"_id": 0}  # Exclude the id field
    
    if file_fields:
        # Create a projection to include only specified file fields
        projection.update({field: 1 for field in file_fields})
    
    data = list(collection.find(query, projection))
    return data

def main(username):
    st.title("Retrieval and Notification Page")

    # Simulate the logged-in user's username
    if "logged_in_username" not in st.session_state:
        st.session_state.logged_in_username = username  # Replace this with actual login logic

    username = st.session_state.logged_in_username
    
    st.text_input("Logged-in Username:", username, disabled=True)
    
    # Date filter inputs
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # Select collection(s) to retrieve data from
    selected_collections = st.multiselect("Select Collection(s)", list(collections_with_files.keys()), default=list(collections_with_files.keys()))

    # Flags to track if data retrieval buttons were clicked
    retrieve_clicked = False
    retrieve_all_clicked = False
    
    # Use st.columns() to place buttons side by side
    col1, col2 = st.columns(2)
    
    # "Retrieve" button
    if col1.button("Retrieve"):
        retrieve_clicked = True
        try:
            for collection_name in selected_collections:
                st.subheader(f"Collection: {collection_name.upper()}")
                
                file_fields = collections_with_files[collection_name]
                data = retrieve_data_from_collection(username, collection_name, start_date, end_date, file_fields)
                
                if not data:
                    st.warning(f"No data found for username '{username}' in collection '{collection_name}'.")
                else:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                    st.write("")  # Empty line for spacing
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # "Retrieve All Data" button
    if col2.button("Retrieve All Data"):
        retrieve_all_clicked = True
        try:
            for collection_name in selected_collections:
                st.subheader(f"Collection: {collection_name.upper()}")
                
                file_fields = collections_with_files[collection_name]
                data = retrieve_data_from_collection(username, collection_name, file_fields=file_fields)
                
                if not data:
                    st.warning(f"No data found for username '{username}' in collection '{collection_name}'.")
                else:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                    st.write("")  # Empty line for spacing
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
