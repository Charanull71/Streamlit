import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_cookies_manager import EncryptedCookieManager
from WTF import help, issues, adminissue,pl,adminpow, proofret,pc,l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, retrieve, facultyretrieve, notification, HODD,HODDPOW, sent, r, pdf
# Set page configuration
st.set_page_config(
    page_title="Employee Appraisal System",  # Title of the page
    page_icon="📝",  # Icon to display in the browser tab (can be an emoji or path to an image file)
    layout="centered"  # Optional: 'wide' for full-width layout, 'centered' for centered layout
)

# Initialize EncryptedCookieManager with required 'password'
cookies = EncryptedCookieManager(password="a$tr0ngP@ssw0rdTh@tIsS3cur3")

# Check if cookies are loaded
if not cookies.ready():
    st.warning("Cookies are not loaded. Please check your configuration.")
    st.stop()  # Stop execution until cookies are ready

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

if "logged_in" not in st.session_state:
    st.session_state.logged_in = cookies.get("logged_in") == "True"

if "username" not in st.session_state:
    st.session_state.username = cookies.get("username")

if "role" not in st.session_state:
    st.session_state.role = cookies.get("role")


if "department" not in st.session_state and st.session_state.username:
    user = db['users'].find_one({"username": st.session_state.username})
    st.session_state.department = user.get("department") if user else ""


def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["HOD", "Faculty", "Principal", "Admin"])

    if st.button("Login"):
        user = db['users'].find_one({"username": username, "password": password, "role": role})
        if user:
            if user.get('role') == "Suspended":
                st.error("You are no longer part of the organization.")
            else:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.role = role

                cookies["logged_in"] = "True"
                cookies["username"] = username
                cookies["role"] = role

                # Save the cookies and rerun the script
                cookies.save()
                st.rerun()
        else:
            st.error("Invalid username, password, or role")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    # Clear cookies by deleting them
    cookies.pop("logged_in", None)
    cookies.pop("username", None)
    cookies.pop("role", None)

    # Save the changes and reload the page to show the login form
    cookies.save()
    st.rerun()
def hod_home():
    st.title(f"Welcome HOD: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Sent", "Retrieved Data", "Pdf View", "Departmental Retrieve", "Departmental POW Retrieve", "Graph"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        st.write("Received Page")
    elif nav == "Sent":
        sent.main()
    elif nav == "Pdf View":
        pdf.main()
    elif nav == "Retrieved Data":
        retrieve.main()
    elif nav == "Departmental Retrieve":
        HODD.main(st.session_state.username)
    elif nav == "Departmental POW Retrieve":
        HODDPOW.main(st.session_state.username, st.session_state.role, st.session_state.department)
    elif nav == "Graph":
        pc.main(st.session_state.username)

def principal_home():
    st.title(f"Welcome Principal: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Pdf View", "Graph", "Sent"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        r.main()
    elif nav == "Pdf View":
        pdf.main()
    elif nav == "Sent":
        st.write("No sent page")
    elif nav == "Graph":
        pc.main(st.session_state.username)

def faculty_home():
    st.image('img.png')
    st.title(f"Welcome Faculty: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    available_pages = ["Help", "THEORY COURSES HANDLED", "STUDENT PROJECT WORKS UNDERTAKEN", "STUDENT TRAINING", "LEARNING MATERIAL", "CERTIFICATE COURSES DONE", "FDPs ATTENDED", "FDPs ORGANIZED", "PROFESSION ROLES", "STUDENT COUNSELLING / MENTORING", "MEMBERSHIPS WITH PROFESSIONAL BODIES", "CHAIRING SESSIONS AND DELIVERING TALKS & LECTURES", "JOURNAL PUBLICATIONS", "CONFERENCE PUBLICATIONS", "RESEARCH GUIDANCE", "BOOK PUBLICATIONS", "PATENTS", "PRODUCT DESIGN / SOFTWARE DEVELOPMENT", "CONSULTANCY", "FUNDED PROJECTS", "FELLOWSHIP/AWARD", "OTHER INFORMATION", "NUMBER OF LEAVES AVAILED", "POW Retrieve", "Retrieve", "Notifications","PDF View", "Graphical Analysis", "Graphical Analysis - Detailed", "Issues"]
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
        pdf.main()
    elif nav == "Issues":
        issues.main(st.session_state.username)

def admin_home():
    st.title("Welcome Admin")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Users", "Suspend User", "Pdf View", "Issues", "POW ADMIN"])

    if nav == "Users":
        adminissue.add_user()
    elif nav == "Suspend User":
        adminissue.suspend_user()
    elif nav == "Pdf View":
        pdf.main()
    elif nav == "Issues":
        adminissue.main()
    elif nav == "POW ADMIN":
        adminpow.main()

@st.cache_data
def get_faculty_details():
    faculty_details = db['users'].find({"role": "Faculty"}, {"_id": 0, "password": 0})
    df = pd.DataFrame(faculty_details)
    return df

def show_faculty_details():
    df = get_faculty_details()
    st.table(df)

if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "HOD":
        hod_home()
    elif st.session_state.role == "Faculty":
        faculty_home()
    elif st.session_state.role == "Principal":
        principal_home()
    elif st.session_state.role == "Admin":
        admin_home()

# Make sure to sync cookies
cookies.save()
