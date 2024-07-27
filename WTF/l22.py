import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l22']
def main(username):
    # st.set_page_config(page_title="Streamlit Leaves Availed Form", page_icon="🌿")

    st.title("LEAVES AVAILED")

    # Date dropdowns for 'From' and 'To' dates
    from_date = st.date_input("From Date")
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
            data = {
                "from_date": from_date.strftime('%Y-%m-%d') if isinstance(from_date, datetime.date) else None,
                "to_date": to_date.strftime('%Y-%m-%d') if isinstance(to_date, datetime.date) else None,
                "classes": classes,
                "hp_classes": hp_classes,
                "c_classes": c_classes,
                "ods": ods,
                "study_leaves": study_leaves,
                "academic_leaves": academic_leaves,
                "permissions": permissions,
                "other_leaves_remarks": other_leaves_remarks,
                "date": datetime.datetime.now()
            }

            collection.insert_one(data)
            st.success("Leaves availed data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

if __name__ == "__main__":
    main(st.session_state.username)