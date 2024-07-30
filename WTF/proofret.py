import streamlit as st
from pymongo import MongoClient
import gridfs
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

# Connect to MongoDB
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

# Collections with file fields and their respective fields
collections_with_files = {
    "l5": "certificate_file",
    "l6": "certificate_file",
    "l8": "certificate_file",
    "l10": "certificate_file",
    "l11": "file_uploader",
    "l12": ["pdf_uploader1", "pdf_uploader2"],
    "l13": "pdf_uploader"
}

def get_collection_list():
    return list(collections_with_files.keys())

def download_file(gridfs_db, file_id):
    fs = gridfs.GridFS(gridfs_db)
    file = fs.get(file_id)
    return file.read()

def main(username):
    st.title("Retrieve Proof of Work PDFs")

    # Select collection
    collection = st.selectbox("Select a Collection", get_collection_list())

    # Date filter
    from_date = st.date_input("From Date", value=datetime(2022, 1, 1))
    to_date = st.date_input("To Date", value=datetime.now())

    if from_date > to_date:
        st.error("From Date cannot be greater than To Date")
        return

    # Convert date to datetime
    from_datetime = datetime.combine(from_date, datetime.min.time())
    to_datetime = datetime.combine(to_date, datetime.max.time())

    # Logging the query
    logging.debug(f"Querying collection: {collection}")
    logging.debug(f"From date: {from_datetime}")
    logging.debug(f"To date: {to_datetime}")
    logging.debug(f"Username: {username}")

    # Fetch data from MongoDB based on selected collection, date filter, and username
    if collection and st.button("Retrieve Data"):
        coll = db[collection]
        query = {
            "username": username,
            "upload_date": {"$gte": from_datetime, "$lte": to_datetime}
        }

        logging.debug(f"Query: {query}")

        try:
            docs = list(coll.find(query))
        except Exception as e:
            logging.error(f"Error querying collection: {e}")
            st.error(f"Error querying collection: {e}")
            return

        logging.debug(f"Number of documents found: {len(docs)}")
        for doc in docs:
            logging.debug(doc)

        if len(docs) == 0:
            st.warning("No records found for the selected criteria.")
            return

        for doc in docs:
            st.write(doc)
            file_fields = collections_with_files[collection]
            if isinstance(file_fields, list):
                for field in file_fields:
                    if field in doc:
                        file_id = doc[field]
                        try:
                            st.download_button(
                                label=f"Download {field}",
                                data=download_file(db, file_id),
                                file_name=f"{collection}_{field}_{str(file_id)}.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            logging.error(f"Error downloading file: {e}")
                            st.error(f"Error downloading file: {e}")
            else:
                if file_fields in doc:
                    file_id = doc[file_fields]
                    try:
                        st.download_button(
                            label=f"Download {file_fields}",
                            data=download_file(db, file_id),
                            file_name=f"{collection}_{file_fields}_{str(file_id)}.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        logging.error(f"Error downloading file: {e}")
                        st.error(f"Error downloading file: {e}")

if __name__ == "__main__":
    if 'username' in st.session_state:
        main(st.session_state.username)
    else:
        st.error("No user logged in. Please log in to retrieve data.")
