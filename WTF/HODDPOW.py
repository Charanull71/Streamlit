import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from PyPDF2 import PdfMerger
import base64
import io

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

# Function to convert date to datetime
def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())

# Function to retrieve data from collection
def retrieve_data_from_collection(username=None, department=None, collection_name=None, start_date=None, end_date=None, file_fields=None):
    collection = db[collection_name]
    query = {}
    
    if username:
        query["username"] = username
    elif department:
        query["department"] = department
    
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

# Function to decode base64 file
def decode_base64_file(encoded_data):
    return base64.b64decode(encoded_data)

# Function to create PDF from decoded files
def create_pdf_from_decoded_files(decoded_files):
    merger = PdfMerger()
    for pdf in decoded_files:
        pdf_stream = io.BytesIO(pdf)
        merger.append(pdf_stream)
    
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    
    return output

# Main function
def main(username, role):
    st.title("Retrieval and Notification Page")

    # Simulate the logged-in user's username and role
    hod_user = db['users'].find_one({"username": username, "role": "HOD"})
    
    if not hod_user:
        st.error("HOD user not found")
        return

    hod_department = hod_user.get("department")
    
    st.text_input("Logged-in Username:", username, disabled=True)
    st.text_input("Role:", role, disabled=True)
    
    # Date filter inputs
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # Select collection(s) to retrieve data from
    selected_collections = st.multiselect("Select Collection(s)", list(collections_with_files.keys()), default=list(collections_with_files.keys()))

    # Use st.columns() to place buttons side by side
    col1, col2, col3 = st.columns(3)
    
    # "Retrieve" button
    if col1.button("Retrieve"):
        try:
            for collection_name in selected_collections:
                st.subheader(f"Collection: {collection_name.upper()}")
                
                file_fields = collections_with_files[collection_name]
                
                if role == "HOD":
                    data = retrieve_data_from_collection(department=hod_department, collection_name=collection_name, start_date=start_date, end_date=end_date, file_fields=file_fields)
                else:
                    data = retrieve_data_from_collection(username=username, collection_name=collection_name, start_date=start_date, end_date=end_date, file_fields=file_fields)
                
                if not data:
                    st.warning(f"No data found in collection '{collection_name}'.")
                else:
                    decoded_files = []
                    for record in data:
                        for field in file_fields:
                            if field in record:
                                encoded_data = record[field]
                                decoded_file = decode_base64_file(encoded_data)
                                decoded_files.append(decoded_file)
                    
                    if decoded_files:
                        pdf_output = create_pdf_from_decoded_files(decoded_files)
                        st.download_button(
                            label=f"Download {collection_name.upper()} PDFs",
                            data=pdf_output.getvalue(),
                            file_name=f"{collection_name}.pdf",
                            mime="application/pdf"
                        )
                    st.write("")  # Empty line for spacing
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # "Retrieve All Data" button
    if col2.button("Retrieve All Data"):
        try:
            for collection_name in selected_collections:
                st.subheader(f"Collection: {collection_name.upper()}")
                
                file_fields = collections_with_files[collection_name]
                
                if role == "HOD":
                    data = retrieve_data_from_collection(department=hod_department, collection_name=collection_name, file_fields=file_fields)
                else:
                    data = retrieve_data_from_collection(username=username, collection_name=collection_name, file_fields=file_fields)
                
                if not data:
                    st.warning(f"No data found in collection '{collection_name}'.")
                else:
                    decoded_files = []
                    for record in data:
                        for field in file_fields:
                            if field in record:
                                encoded_data = record[field]
                                decoded_file = decode_base64_file(encoded_data)
                                decoded_files.append(decoded_file)
                    
                    if decoded_files:
                        pdf_output = create_pdf_from_decoded_files(decoded_files)
                        st.download_button(
                            label=f"Download {collection_name.upper()} PDFs",
                            data=pdf_output.getvalue(),
                            file_name=f"{collection_name}.pdf",
                            mime="application/pdf"
                        )
                    st.write("")  # Empty line for spacing
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    if col3:
        st.write("")

if __name__ == "__main__":
    main(st.session_state.username,st.session_state.role,st.session_state.department)  # Replace with dynamic username, role, and department retrieval logic if available
