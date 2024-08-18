import streamlit as st
import datetime
from pymongo import MongoClient
from l1 import pascal_case
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l22']
collection_users = db['users']
def main(username):
    # st.set_page_config(page_title="Streamlit Leaves Availed Form", page_icon="🌿")

    st.title("LEAVES AVAILED")

    # Date dropdowns for 'From' and 'To' dates
    col1,col2 =st.columns(2)
    with col1:
        from_date = st.date_input("From Date")
    with col2:
        to_date = st.date_input("To Date")

    classes = st.number_input("Cls", min_value=0, step=1, value=0, key="classes")
    hp_classes = st.number_input("HP Cls", min_value=0, step=1, value=0, key="hp_classes")
    c_classes = st.number_input("C Cls", min_value=0, step=1, value=0, key="c_classes")
    ods = st.number_input("ODs", min_value=0, step=1, value=0, key="ods")
    study_leaves = st.number_input("Study leaves", min_value=0, step=1, value=0, key="study_leaves")
    academic_leaves = st.number_input("Academic leaves", min_value=0, step=1, value=0, key="academic_leaves")
    permissions = st.number_input("No. of permissions", min_value=0, step=1, value=0, key="permissions")
    other_leaves_remarks = st.text_area("Any other leaves & remarks", "", key="other_leaves_remarks")

    if st.button("Submit"):
        # Validate and store leaves availed details in MongoDB
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
                "from_date": from_date.strftime('%Y-%m-%d') if isinstance(from_date, datetime.date) else None,
                "to_date": to_date.strftime('%Y-%m-%d') if isinstance(to_date, datetime.date) else None,
                "classes": classes,
                "hp_classes": hp_classes,
                "c_classes": c_classes,
                "ods": ods,
                "study_leaves": study_leaves,
                "academic_leaves": academic_leaves,
                "permissions": permissions,
                "other_leaves_remarks": pascal_case(other_leaves_remarks),
                "date": datetime.datetime.now()
            }

            collection.insert_one(data)
            st.success("Leaves availed data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

if __name__ == "__main__":
    main(st.session_state.username)