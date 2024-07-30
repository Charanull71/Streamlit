import streamlit as st
import datetime
from pymongo import MongoClient
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l8']  # Replace 'l8' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

# Define points for various roles
points_dict = {
    "Principal": 100,
    "Vice Principal": 100,
    "Dean": 90,
    "Assoc. Dean": 90,
    "HOD": 80,
    "College level section Incharge": 80,
    "BoS Incharge": 50,
    "Library Incharge": 50,
    "Project Co-Ordinator": 50,
    "Committee Membership": 10
}

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()

    with st.form("l8"):
        st.title("Professional Roles")

        # College level roles
        st.write("**College level (Principal, Vice Principal, Deans etc)**")
        college_role = st.selectbox("Select College Level Role", ["None", "Principal", "Vice Principal", "Dean", "Assoc. Dean"], key="college_role")
        
        if college_role != "None":
            college_role_nature_of_work = st.text_input("Nature of work", key="college_role_nature_of_work")
            college_role_since = st.date_input("SINCE DATE", today, format="MM/DD/YYYY", key="college_role_since")
            college_role_till = st.date_input("TILL DATE", today, format="MM/DD/YYYY", key="college_role_till")
            st.write(f"**Role:** {college_role}")
            st.write(f"**Nature of Work:** {college_role_nature_of_work}")
            st.write(f"**Since Date:** {college_role_since.strftime('%Y-%m-%d')}")
            st.write(f"**Till Date:** {college_role_till.strftime('%Y-%m-%d')}")
            st.write(f"**Points:** {points_dict[college_role]}")
        else:
            college_role_nature_of_work = college_role_since = college_role_till = None

        # Department level roles
        st.write("**Department level (HODs, College level section Incharges)**")
        department_role = st.selectbox("Select Department Level Role", ["None", "HOD", "College level section Incharge"], key="department_role")
        
        if department_role != "None":
            department_name = st.text_input("Department", key="department_name")
            department_nature_of_work = st.text_input("Nature of work", key="department_nature_of_work")
            department_since = st.date_input("SINCE DATE", today, format="MM/DD/YYYY", key="department_since")
            department_till = st.date_input("TILL DATE", today, format="MM/DD/YYYY", key="department_till")
            st.write(f"**Role:** {department_role}")
            st.write(f"**Department:** {department_name}")
            st.write(f"**Nature of Work:** {department_nature_of_work}")
            st.write(f"**Since Date:** {department_since.strftime('%Y-%m-%d')}")
            st.write(f"**Till Date:** {department_till.strftime('%Y-%m-%d')}")
            st.write(f"**Points:** {points_dict[department_role]}")
        else:
            department_name = department_nature_of_work = department_since = department_till = None

        # Incharges & Committee Coordinators
        st.write("**Department level Incharges & College level Committee Coordinators**")
        incharges = []
        incharge_roles = ["BoS Incharge", "Library Incharge", "Project Co-Ordinator"]
        
        for incharge in incharge_roles:
            incharge_role = st.selectbox(f"Select Incharge Role ({incharge})", ["None", incharge], key=f"incharge_role_{incharge}")
            
            if incharge_role != "None":
                incharge_since = st.date_input(f"SINCE DATE ({incharge})", today, format="MM/DD/YYYY", key=f"incharge_since_{incharge}")
                incharge_till = st.date_input(f"TILL DATE ({incharge})", today, format="MM/DD/YYYY", key=f"incharge_till_{incharge}")
                st.write(f"**Role:** {incharge}")
                st.write(f"**Since Date:** {incharge_since.strftime('%Y-%m-%d')}")
                st.write(f"**Till Date:** {incharge_till.strftime('%Y-%m-%d')}")
                st.write(f"**Points:** {points_dict[incharge]}")
                incharges.append({
                    "role": incharge,
                    "since_date": incharge_since.strftime("%Y-%m"),
                    "till_date": incharge_till.strftime("%Y-%m"),
                    "points": points_dict[incharge]
                })

        # Committee Memberships
        st.write("**CURRENTLY engaged Committee Memberships**")
        membership_role = st.selectbox("Select Committee Membership", ["None", "Committee Membership"], key="membership_role")
        memberships = []
        if membership_role != "None":
            membership_nature_of_work = st.text_input("Nature of work", key="membership_nature_of_work")
            membership_since = st.date_input("SINCE DATE", today, format="MM/DD/YYYY", key="membership_since")
            membership_till = st.date_input("TILL DATE", today, format="MM/DD/YYYY", key="membership_till")
            st.write(f"**Nature of Work:** {membership_nature_of_work}")
            st.write(f"**Since Date:** {membership_since.strftime('%Y-%m-%d')}")
            st.write(f"**Till Date:** {membership_till.strftime('%Y-%m-%d')}")
            st.write(f"**Points:** {points_dict[membership_role]}")
            memberships.append({
                "nature_of_work": membership_nature_of_work,
                "since_date": membership_since.strftime("%Y-%m"),
                "till_date": membership_till.strftime("%Y-%m"),
                "points": points_dict[membership_role]
            })

        # File uploader for certificates
        certificate_file = st.file_uploader("Upload your all role certificate PDF", type=["pdf"])

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if (college_role == "None" and department_role == "None" and
                not incharges and not memberships):
                st.error("Please fill out at least one required field.")
                return

            if not certificate_file:
                st.error("Please upload your certificate PDF.")
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

                # Read the file content and encode it in base64
                certificate_content = certificate_file.read()
                encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')

                # Calculate total points
                total_points = 0
                if college_role != "None":
                    total_points += points_dict[college_role]
                if department_role != "None":
                    total_points += points_dict[department_role]
                total_points += sum(incharge['points'] for incharge in incharges)
                total_points += sum(membership['points'] for membership in memberships)
                total_points = min(total_points, 100)  # Ensure the total points do not exceed the maximum

                data = {
                    "username": username,
                    "college_role": college_role,
                    "department": department_role,
                    "incharges": incharges,
                    "memberships": memberships,
                    "department": department,
                    "certificate_file": encoded_certificate,
                    "total_points": total_points,
                    "date": datetime.datetime.now()
                }

                # Insert data into MongoDB
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
