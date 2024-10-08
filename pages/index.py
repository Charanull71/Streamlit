import streamlit as st
from pymongo import MongoClient
import pandas as pd
import importlib
# import toml
from WTF import help, issues, adminissue,pl,adminpow, proofret,pc,l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, retrieve, facultyretrieve, notification, HODD,HODDPOW, sent, r, adman,pdf,pdetails
# Hide the Streamlit hamburger menu and footer
st.markdown("""
    <style>
            #MainMenu{visibility: hidden;}
        .st-emotion-cache-1wbqy5l e3g6aar2{
            display: none !important;
            visibility: hidden;
        }
        .st-emotion-cache-1huvf7z ef3psqc5{
            display: none !important;
            visibility: hidden;
        }
        .st-emotion-cache-1huvf7z ef3psqc6{
            display: none important;
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

# Session state for managing login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# Login logic
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Super Admin", "Admin", "HOD", "Faculty", "Principal"])

    organisation = ""
    if role in ["Admin", "HOD", "Faculty", "Principal"]:
        # Retrieve the list of organisations from the database for the dropdown
        organisations = [org['org_name'] for org in db['organisations'].find()]
        
        if organisations:
            organisation = st.selectbox("Organisation", organisations)
        else:
            st.error("No organisations found in the database. Please contact the Super Admin.")

    if st.button("Login"):
        if username == "superadmin" and password == "123456" and role == "Super Admin":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.password = password
            st.session_state.role = role
            st.rerun()
        else:
            user = db['users'].find_one({"username": username, "password": password, "role": role, "organisation": organisation})
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.role = role
                st.session_state.organisation = organisation
                st.rerun()
            else:
                st.error("Invalid username, password, role, or organisation.")

# Super Admin Home Page
def super_admin_home():
    st.title(f"Welcome Super Admin: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Super Admin Menu", ["Add Organisation", "Add Admin", "Manage Organisations", "Manage Admins"])

    if nav == "Add Organisation":
        add_organisation()
    elif nav == "Add Admin":
        add_admin()
    elif nav == "Manage Organisations":
        manage_organisations()
    elif nav == "Manage Admins":
        manage_admins()

# Adding a new organisation
def add_organisation():
    st.header("Add New Organisation")
    
    org_name = st.text_input("Organisation Name")
    director_number = st.text_input("Director Contact Number")
    principal_number = st.text_input("Principal Contact Number")
    employee_count = st.number_input("Number of Employees", min_value=1)

    if st.button("Add Organisation"):
        if org_name and director_number and principal_number and employee_count > 0:
            org_data = {
                "org_name": org_name,
                "director_number": director_number,
                "principal_number": principal_number,
                "employee_count": employee_count
            }
            db['organisations'].insert_one(org_data)
            st.success(f"Organisation '{org_name}' added successfully!")
        else:
            st.warning("Please fill in all fields.")

# Adding a new admin for an organisation
def add_admin():
    st.header("Add New Admin")

    organisations = [org['org_name'] for org in db['organisations'].find()]
    admin_username = st.text_input("Admin Username")
    admin_password = st.text_input("Admin Password", type="password")
    selected_org = st.selectbox("Organisation", organisations)

    if st.button("Create Admin"):
        if admin_username and admin_password and selected_org:
            new_admin = {
                "username": admin_username,
                "password": admin_password,
                "role": "Admin",
                "organisation": selected_org,
                "status": "Active"
            }
            db['users'].insert_one(new_admin)
            st.success(f"Admin '{admin_username}' created for organisation '{selected_org}'!")
        else:
            st.warning("Please fill in all fields.")

# Managing existing organisations
def manage_organisations():
    st.header("Manage Organisations")

    orgs = db['organisations'].find()
    for org in orgs:
        st.write(f"*Organisation Name:* {org['org_name']}")
        st.write(f"Director Contact: {org['director_number']}")
        st.write(f"Principal Contact: {org['principal_number']}")
        st.write(f"Employee Count: {org['employee_count']}")

        if st.button(f"Remove {org['org_name']}"):
            db['organisations'].delete_one({"org_name": org['org_name']})
            st.success(f"Organisation '{org['org_name']}' removed.")
            st.rerun()

# Managing admins
def manage_admins():
    st.header("Manage Admins")

    admins = db['users'].find({"role": "Admin"})
    for admin in admins:
        st.write(f"*Admin Username:* {admin['username']}")
        organisation = admin.get('organisation', 'Not Assigned')
        st.write(f"Organisation: {organisation}")

        if st.button(f"Remove Admin {admin['username']}"):
            db['users'].delete_one({"username": admin['username']})
            st.success(f"Admin '{admin['username']}' removed.")
            st.rerun()

# Admin, HOD, Faculty, Principal home pages
def admin_home():
    st.write(f"Welcome Admin: {st.session_state.username}")
    st.title(f"Welcome Admin: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()
    nav = st.sidebar.radio("Navigation", ["Add User", "Suspend User","Issues","Add Fields","Delete Fields"])
    if nav == "Add User":
        add_user_form()
    elif nav == "Suspend User":
        suspend_user_form()
    elif nav == "Issues":
        adminissue.main()
    elif nav == "Add Fields":
        adman.main()
def add_user_form():
    st.header("Add New User")
    
    # Retrieve the organization of the logged-in admin
    organisation = db['users'].find_one({"username": st.session_state.username})['organisation']

    with st.form("add_user_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["Faculty", "HOD", "Principal"])
        new_department = st.text_input("Department")
        
        # Display the organization name (non-modifiable input)
        st.text_input("Organisation", value=organisation, disabled=True)
        
        submit_button = st.form_submit_button("Add User")
        
        if submit_button:
            if new_username and new_password and new_role and new_department:
                new_user = {
                    "username": new_username,
                    "password": new_password,
                    "role": new_role,
                    "department": new_department,
                    "organisation": organisation,  # Set the organisation from logged-in admin
                    "status": "Active"  # Default status
                }
                try:
                    db['users'].insert_one(new_user)
                    st.success("User added successfully!")
                except Exception as e:
                    st.error(f"Error adding user: {e}")
            else:
                st.warning("Please fill in all fields.")

def suspend_user_form():
    st.header("Suspend User")
    with st.form("suspend_user_form"):
        suspend_username = st.text_input("Username to Suspend")
        submit_button = st.form_submit_button("Suspend User")
        if submit_button:
            if suspend_username:
                try:
                    result = db['users'].update_one(
                        {"username": suspend_username},
                        {"$set": {"role": "Suspended"}}
                    )
                    if result.matched_count > 0:
                        st.success(f"User '{suspend_username}' has been suspended successfully!")
                    else:
                        st.warning(f"User '{suspend_username}' not found.")
                except Exception as e:
                    st.error(f"Error suspending user: {e}")
            else:
                st.warning("Please enter a username.")
def show_faculty_details():
    # Retrieve the department of the logged-in HOD
    if st.session_state.role == "HOD":
        hod_department = db['users'].find_one({"username": st.session_state.username})['department']
        # Filter users based on the HOD's department
        users = db['users'].find({"department": hod_department})
        
        # Define the columns to display
        columns_to_display = ["username", "role", "department"]
    else:
        # For other roles, display all users
        users = db['users'].find()
        columns_to_display = ["username", "password", "role", "department"]
    
    # Convert the result to a DataFrame
    df = pd.DataFrame(list(users), columns=["username", "password", "role", "department"])
    
    # Display the DataFrame with selected columns
    st.write(df[columns_to_display])


def hod_home():
    st.title(f"Welcome HOD: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Sent", "Retrieved Data", "Pdf View", "Departmental Retrieve", "Departmental POW Retrieve", "Graph","Personal Details"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        st.write("Received Page")
    elif nav == "Sent":
        sent.main()
    elif nav == "Pdf View":
        pdf.main(st.session_state.username,st.session_state.role)
    elif nav == "Retrieved Data":
        retrieve.main()
    elif nav == "Departmental Retrieve":
        HODD.main(st.session_state.username)
    elif nav == "Departmental POW Retrieve":
        HODDPOW.main(st.session_state.username, st.session_state.role)
    elif nav == "Graph":
        pc.main(st.session_state.username)


def faculty_home():
    #st.write(f"Welcome Faculty: {st.session_state.username}")
    st.image('img.png')
    st.title(f"Welcome Faculty: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()
    available_pages = ["Help", "THEORY COURSES HANDLED", "STUDENT PROJECT WORKS UNDERTAKEN", "STUDENT TRAINING", "LEARNING MATERIAL", "CERTIFICATE COURSES DONE", "FDPs ATTENDED", "FDPs ORGANIZED", "PROFESSION ROLES", "STUDENT COUNSELLING / MENTORING", "MEMBERSHIPS WITH PROFESSIONAL BODIES", "CHAIRING SESSIONS AND DELIVERING TALKS & LECTURES", "JOURNAL PUBLICATIONS", "CONFERENCE PUBLICATIONS", "RESEARCH GUIDANCE", "BOOK PUBLICATIONS", "PATENTS", "PRODUCT DESIGN / SOFTWARE DEVELOPMENT", "CONSULTANCY", "FUNDED PROJECTS", "FELLOWSHIP/AWARD", "OTHER INFORMATION", "NUMBER OF LEAVES AVAILED", "POW Retrieve", "Retrieve", "Notifications","PDF View", "Graphical Analysis", "Graphical Analysis - Detailed", "Issues","Personal Details"]
    nav = st.sidebar.radio("Navigation", available_pages)
    if nav == "Help":
        help.main()
    elif nav == "THEORY COURSES HANDLED":
        l1.main(st.session_state.username)
    elif nav == "STUDENT PROJECT WORKS UNDERTAKEN":
        l2.main(st.session_state.username)
    elif nav == "STUDENT TRAINING":
        l3.main(st.session_state.username)
    elif nav == "LEARNING MATERIAL":
        l4.main(st.session_state.username)
    elif nav == "CERTIFICATE COURSES DONE":
        l5.main(st.session_state.username)
    elif nav == "FDPs ATTENDED":
        l6.main(st.session_state.username)
    elif nav == "FDPs ORGANIZED":
        l7.main(st.session_state.username)
    elif nav == "PROFESSION ROLES":
        l8.main(st.session_state.username)
    elif nav == "STUDENT COUNSELLING / MENTORING":
        l9.main(st.session_state.username)
    elif nav == "MEMBERSHIPS WITH PROFESSIONAL BODIES":
        l10.main(st.session_state.username)
    elif nav == "CHAIRING SESSIONS AND DELIVERING TALKS & LECTURES":
        l11.main(st.session_state.username)
    elif nav == "JOURNAL PUBLICATIONS":
        l12.main(st.session_state.username)
    elif nav == "CONFERENCE PUBLICATIONS":
        l13.main(st.session_state.username)
    elif nav == "RESEARCH GUIDANCE":
        l14.main(st.session_state.username)
    elif nav == "BOOK PUBLICATIONS":
        l15.main(st.session_state.username)
    elif nav == "PATENTS":
        l16.main(st.session_state.username)
    elif nav == "PRODUCT DESIGN / SOFTWARE DEVELOPMENT":
        l17.main(st.session_state.username)
    elif nav == "CONSULTANCY":
        l18.main(st.session_state.username)
    elif nav == "FUNDED PROJECTS":
        l19.main(st.session_state.username)
    elif nav == "FELLOWSHIP/AWARD":
        l20.main(st.session_state.username)
    elif nav == "OTHER INFORMATION":
        l21.main(st.session_state.username)
    elif nav == "NUMBER OF LEAVES AVAILED":
        l22.main(st.session_state.username)
    elif nav == "POW Retrieve":
        proofret.main(st.session_state.username)
    elif nav == "Retrieve":
        facultyretrieve.main(st.session_state.username)
    elif nav == "Notifications":
        notification.main(st.session_state.username)
    elif nav == "PDF View":
        pdf.main(st.session_state.username,st.session_state.role)
    elif nav == "Issues":
        issues.main(st.session_state.username)
    elif nav == "Graphical Analysis":
        pl.main(st.session_state.username)
    elif nav == "Graphical Analysis - Detailed":
        pc.main(st.session_state.username)
    elif nav == "Personal Details":
        pdetails.main()
    

def principal_home():

    st.title(f"Welcome Principal: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Pdf View", "Graph"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        r.main()
    elif nav == "Pdf View":
        pdf.main(st.session_state.username,st.session_state.role)
    elif nav == "Sent":
        st.write("No sent page")
    elif nav == "Graph":
        pc.main(st.session_state.username)

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

# Main logic
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "Super Admin":
        super_admin_home()
    elif st.session_state.role == "Admin":
        admin_home()
    elif st.session_state.role == "HOD":
        hod_home()
    elif st.session_state.role == "Faculty":
        faculty_home()
    elif st.session_state.role == "Principal":
        principal_home()