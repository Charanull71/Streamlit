import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd
from .l1 import pascal_case
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l16']  # Replace 'l16' with your actual collection name
collection_users = db['users']

# Define points for each patent type


def calculate_points(patent_type, patent_category):
    PATENT_POINTS = {
    "Obtained": {
        "International": 100,
        "National": 80,
        "State": 60,
        "Local": 40
    },
    "Filed": {
        "International": 80,
        "National": 60,
        "State": 40,
        "Local": 20
    }
    }
    return PATENT_POINTS[patent_type].get(patent_category, 0)

def main(username):
    st.title("PATENTS")

    with st.form("l16"):
        # Section for patents filed/obtained up to previous assessment year
        st.subheader("No. Of PATENTS Filed/Obtained up to previous assessment year")
        n1 = st.text_input("No. Of PATENTS Filed:", value="", placeholder="Enter number of patents filed up to previous assessment year")
        n2 = st.text_input("No. Of PATENTS Obtained:", value="", placeholder="Enter number of patents obtained up to previous assessment year")

        # Section for patents filed/obtained in present assessment year
        st.subheader("No. Of PATENTS Filed/Obtained in present assessment year")
        col1,col2=st.columns(2)
        with col1:
            status_of_patent = st.selectbox("Status of Patent", ["", "Filed", "Obtained"])
        with col2:
            level_of_patent = st.selectbox("Level of Patent", ["", "International", "National", "State", "Local"])
        date_of_filing = st.date_input("Date of Filing", value=datetime.datetime.now(), format="YYYY-MM-DD")
        description_of_patent = st.text_area("Description of Patent", value="", placeholder="Enter description of the patent")

        if status_of_patent and level_of_patent:
            points = calculate_points(status_of_patent, level_of_patent)
        else:
            points = 0
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and n2 and status_of_patent and level_of_patent and description_of_patent):
                st.error("Please fill out all required fields.")
                return

            try:
                # Convert date to datetime.datetime
                date_of_filing = datetime.datetime.combine(date_of_filing, datetime.datetime.min.time())

                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return

                data = {
                    "username": username,
                    "patents_filed_previous": n1,
                    "patents_obtained_previous": n2,
                    "status_of_patent": status_of_patent,
                    "level_of_patent": level_of_patent,
                    "date_of_filing": date_of_filing,
                    "description_of_patent": pascal_case(description_of_patent),
                    "department": department,
                    "points": points,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        st.subheader("Patents Filed/Obtained This Year")
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