import streamlit as st
import pandas as pd
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l1']

def calpoints(option1, option2, res):
    # Logic to calculate points based on feedback and result percentage
    if option1 == "Excellent" and option2 == "Excellent":
        if int(res) >= 90:
            return 100
        elif int(res) >= 80:
            return 90
        elif int(res) >= 70:
            return 80
        else:
            return 70
    elif option1 == "Good" and option2 == "Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option2 == "Good" and option1 == "Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option1 == "Satisfactory" and option2 == "Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option2 == "Satisfactory" and option1 == "Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1 == "Good" and option2 == "Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option2 == "Good" and option1 == "Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option1 == "Good" and option2 == "Good":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1 == "Satisfactory" and option2 == "Satisfactory":
        if int(res) >= 90:
            return 80
        elif int(res) >= 80:
            return 70
        elif int(res) >= 70:
            return 60
        else:
            return 50

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = True

    # Display warning message for 20 seconds
    # warning_message = "Before submitting, please cross check all of your information is correct and no errors, changes cannot be recognized faster!! We appreciate your careful behavior in your self-appraisal."
    # with st.spinner("Read Warning Message.... "):
    #     st.warning(warning_message, icon="⚠️")
    #     time.sleep(20)  # Wait for 20 seconds

    # Reset session state after 20 seconds
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

    st.title("Theory Courses Handled")
    Subject = st.text_input("Subject", value="", placeholder="Enter Your Subject", disabled=st.session_state.disabled)
    # section = st.text_input("Class & Section", value="", placeholder="Enter Classname & Section || Example: 3 CSE B", disabled=st.session_state.disabled)
    
    col1,col2,col3= st.columns(3)
    with col1:
        year = st.selectbox(
        "Year",
        ("1", "2", "3","4"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
        
        # st.text_input("Year", value="", placeholder="Year Name", disabled=st.session_state.disabled)
    with col2:
        dep =st.selectbox(
        "Department",
        ("CSE", "CSM", "CSD","ECE","EEE","IT","MECH","CIVIL"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    ) 

        # st.text_input("Department", value="", placeholder="Department Name", disabled=st.session_state.disabled)
    with col3:
        section = st.selectbox(
        "Section",
        ("A", "B", "C","D","E","F",),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    ) 
        # st.text_input("Section", value="", placeholder="Enter Classname & Section || Example: 3 CSE B", disabled=st.session_state.disabled)
    col2, col3 = st.columns(2)
    with col2:
        cp = st.text_input("Classes Planned", value="", placeholder="No. Of Classes Planned", disabled=st.session_state.disabled)
    with col3:
        ch = st.text_input("Classes Held", value="", placeholder="No. Of Classes Held", disabled=st.session_state.disabled)

    
    # section = st.text_input("Class & Section", value="", placeholder="Enter Classname & Section || Example: 3 CSE B", disabled=st.session_state.disabled)
    # cp = st.text_input("Classes Planned", value="", placeholder="No. Of Classes Planned", disabled=st.session_state.disabled)
    # ch = st.text_input("Classes Held", value="", placeholder="No. Of Classes Held", disabled=st.session_state.disabled)
    col4, col5 = st.columns(2)
    with col4:
        option1 = st.selectbox(
        "Student Feedback (Cycle 1)",
        ("Excellent", "Good", "Satisfactory"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
    with col5:
        option2 = st.selectbox(
        "Student Feedback (Cycle 2)",
        ("Excellent", "Good", "Satisfactory"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
    res = st.text_input("Result Of Students", value="", placeholder="% Of Students Passed", disabled=st.session_state.disabled)

    if st.button("Submit", disabled=st.session_state.disabled):
        # Check for empty fields
        if not (Subject and dep and section and cp and ch and res):
            st.error("Please fill out all fields.")
            return

        try:
            points = calpoints(option1, option2, res)
            data = {
                "username": username,
                "subject": Subject,
                "department": dep,
                "section": year+" "+dep+" "+section,
                "classes_planned": cp,
                "classes_held": ch,
                "feedback1": option1,
                "feedback2": option2,
                "result": res,
                "points": points,
                "date":datetime.datetime.now()
            }
            collection.insert_one(data)
            st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    st.subheader("Courses Handled This Year")
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
