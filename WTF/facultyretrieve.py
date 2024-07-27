import streamlit as st
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import base64
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection_users = db['users']
collection1 = db['l1']
collection4 = db['l4']
collection5 = db['l5']
collection6 = db['l6']
collection7 = db['l7']
collection8 = db['l8']
collection10 = db['l10']
collection11 = db['l11']
collection12 = db['l12']
# Function to calculate points for l1
def calpoints(option1, option2, res):
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

# Function to calculate points for l4
def get_points_l4(material_type, involvement_type):
    if material_type == "ICT Based teaching Material":
        if involvement_type == "Single":
            return 100
        elif involvement_type == "More than one":
            return 50
    elif material_type == "Interactive Courses/Online Courses":
        if involvement_type == "Single":
            return 75
        elif involvement_type == "More than one":
            return 35
    elif material_type == "Participatory Learning Modules/Teaching Notes":
        if involvement_type == "Single":
            return 50
        elif involvement_type == "More than one":
            return 25
    return 0
def get_points_l5(certificate_type, relevance):
    """
    Function to get the points based on the type of certificate and relevance to the field of specialization.
    """
    if certificate_type == "Certificate course/Online certificate/MOOCs course offered by Foreign Universities":
        return 100 if relevance == "Yes" else 50
    elif certificate_type == "Certificate course/Online certificate/MOOCs course offered by IIT/NIT":
        return 75 if relevance == "Yes" else 35
    elif certificate_type == "Certificate course/Online certificate/MOOCs course offered by lower than IIT/NIT institutes or universities":
        return 50 if relevance == "Yes" else 25
    return 0
def get_points_l6(level_of_institute, duration):
    """
    Function to get the points based on the level of institute and duration of the FDP.
    """
    if level_of_institute == "IIT":
        if duration == ">=2W":
            return 100
        elif duration == "1W-2W":
            return 90
        elif duration == "<1W":
            return 80
    elif level_of_institute == "NIT":
        if duration == ">=2W":
            return 90
        elif duration == "1W-2W":
            return 80
        elif duration == "<1W":
            return 70
    elif level_of_institute == "University":
        if duration == ">=2W":
            return 80
        elif duration == "1W-2W":
            return 70
        elif duration == "<1W":
            return 60
    elif level_of_institute == "College":
        if duration == ">=2W":
            return 70
        elif duration == "1W-2W":
            return 60
        elif duration == "<1W":
            return 50
    return 0
def get_points_l7(fdp_type, funding_type, capacity):
    points_dict = {
        # International (>=2W)
        ("International (>=2W)", "External", "Convenor"): 100,
        ("International (>=2W)", "External", "Co-convenor"): 50,
        ("International (>=2W)", "External", "Sponsor"): 90,
        ("International (>=2W)", "External", "Internal"): 80,
        ("International (>=2W)", "Sponsor", "Convenor"): 90,
        ("International (>=2W)", "Sponsor", "Co-convenor"): 45,
        ("International (>=2W)", "Sponsor", "Sponsor"): 80,
        ("International (>=2W)", "Sponsor", "Internal"): 70,
        ("International (>=2W)", "Internal", "Convenor"): 80,
        ("International (>=2W)", "Internal", "Co-convenor"): 40,
        ("International (>=2W)", "Internal", "Sponsor"): 70,
        ("International (>=2W)", "Internal", "Internal"): 60,

        # National (>=2W)
        ("National (>=2W)", "External", "Convenor"): 90,
        ("National (>=2W)", "External", "Co-convenor"): 45,
        ("National (>=2W)", "External", "Sponsor"): 80,
        ("National (>=2W)", "External", "Internal"): 70,
        ("National (>=2W)", "Sponsor", "Convenor"): 80,
        ("National (>=2W)", "Sponsor", "Co-convenor"): 40,
        ("National (>=2W)", "Sponsor", "Sponsor"): 70,
        ("National (>=2W)", "Sponsor", "Internal"): 60,
        ("National (>=2W)", "Internal", "Convenor"): 70,
        ("National (>=2W)", "Internal", "Co-convenor"): 35,
        ("National (>=2W)", "Internal", "Sponsor"): 60,
        ("National (>=2W)", "Internal", "Internal"): 50,

        # International (1W to 2W)
        ("International (1W to 2W)", "External", "Convenor"): 90,
        ("International (1W to 2W)", "External", "Co-convenor"): 45,
        ("International (1W to 2W)", "External", "Sponsor"): 80,
        ("International (1W to 2W)", "External", "Internal"): 70,
        ("International (1W to 2W)", "Sponsor", "Convenor"): 80,
        ("International (1W to 2W)", "Sponsor", "Co-convenor"): 40,
        ("International (1W to 2W)", "Sponsor", "Sponsor"): 70,
        ("International (1W to 2W)", "Sponsor", "Internal"): 60,
        ("International (1W to 2W)", "Internal", "Convenor"): 70,
        ("International (1W to 2W)", "Internal", "Co-convenor"): 35,
        ("International (1W to 2W)", "Internal", "Sponsor"): 60,
        ("International (1W to 2W)", "Internal", "Internal"): 50,

        # National (1W to 2W)
        ("National (1W to 2W)", "External", "Convenor"): 80,
        ("National (1W to 2W)", "External", "Co-convenor"): 40,
        ("National (1W to 2W)", "External", "Sponsor"): 70,
        ("National (1W to 2W)", "External", "Internal"): 60,
        ("National (1W to 2W)", "Sponsor", "Convenor"): 70,
        ("National (1W to 2W)", "Sponsor", "Co-convenor"): 35,
        ("National (1W to 2W)", "Sponsor", "Sponsor"): 60,
        ("National (1W to 2W)", "Sponsor", "Internal"): 50,
        ("National (1W to 2W)", "Internal", "Convenor"): 60,
        ("National (1W to 2W)", "Internal", "Co-convenor"): 30,
        ("National (1W to 2W)", "Internal", "Sponsor"): 50,
        ("National (1W to 2W)", "Internal", "Internal"): 40,

        # International (<1W)
        ("International (<1W)", "External", "Convenor"): 80,
        ("International (<1W)", "External", "Co-convenor"): 40,
        ("International (<1W)", "External", "Sponsor"): 70,
        ("International (<1W)", "External", "Internal"): 60,
        ("International (<1W)", "Sponsor", "Convenor"): 70,
        ("International (<1W)", "Sponsor", "Co-convenor"): 35,
        ("International (<1W)", "Sponsor", "Sponsor"): 60,
        ("International (<1W)", "Sponsor", "Internal"): 50,
        ("International (<1W)", "Internal", "Convenor"): 60,
        ("International (<1W)", "Internal", "Co-convenor"): 30,
        ("International (<1W)", "Internal", "Sponsor"): 50,
        ("International (<1W)", "Internal", "Internal"): 40,

        # National (<1W)
        ("National (<1W)", "External", "Convenor"): 70,
        ("National (<1W)", "External", "Co-convenor"): 35,
        ("National (<1W)", "External", "Sponsor"): 60,
        ("National (<1W)", "External", "Internal"): 50,
        ("National (<1W)", "Sponsor", "Convenor"): 60,
        ("National (<1W)", "Sponsor", "Co-convenor"): 30,
        ("National (<1W)", "Sponsor", "Sponsor"): 50,
        ("National (<1W)", "Sponsor", "Internal"): 40,
        ("National (<1W)", "Internal", "Convenor"): 50,
        ("National (<1W)", "Internal", "Co-convenor"): 25,
        ("National (<1W)", "Internal", "Sponsor"): 40,
        ("National (<1W)", "Internal", "Internal"): 30,
    }
    
    return points_dict.get((fdp_type, funding_type, capacity), 0)
def get_points_l10(membership_type):
    if membership_type == "International Membership":
        return 50
    elif membership_type == "National Membership":
        return 25
    return 0
def get_points_l11(event_type):
    points_dict = {
        "Chaired or Co-chaired (International)": 100,
        "Chaired or Co-chaired (National)": 80,
        "Delivering talks & Lectures (International)": 90,
        "Delivering talks & Lectures (National IIT/NIT Level)": 70,
        "Delivering talks & Lectures (University Level)": 50,
        "Delivering talks & Lectures (College Level)": 40
    }
    return points_dict.get(event_type, 0)

def get_points_l12(journal_type, authorship_position):
    points_dict = {
        "SCI or equivalent": {"1st author": 100, "other": 20},
        "UGC referred Journals": {"1st author": 90, "other": 20},
        "Other International Journals": {"1st author": 80, "other": 10},
        "Other National Journals": {"1st author": 70, "other": 10}
    }
    return points_dict.get(journal_type, {}).get(authorship_position, 0)
# Function to fetch all data from collection1
def fetch_all_data_collection1(username):
    return list(collection1.find({"username": username}))

# Function to fetch row data from collection1
def fetch_row_data_collection1(row_id):
    return collection1.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection1
def update_data_collection1(row_id, new_data):
    try:
        update_result = collection1.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False

# Function to fetch all data from collection4
def fetch_all_data_collection4(username):
    return list(collection4.find({"username": username}))

# Function to fetch row data from collection4
def fetch_row_data_collection4(row_id):
    return collection4.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection4
def update_data_collection4(row_id, new_data):
    try:
        update_result = collection4.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection5(username):
    return list(collection5.find({"username": username}))

# Function to fetch row data from collection4
def fetch_row_data_collection5(row_id):
    return collection5.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection4
def update_data_collection5(row_id, new_data):
    try:
        update_result = collection5.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection6(username):
    return list(collection6.find({"username": username}))

# Function to fetch row data from collection6
def fetch_row_data_collection6(row_id):
    return collection6.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection6
def update_data_collection6(row_id, new_data):
    try:
        update_result = collection6.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection7(username):
    return list(collection7.find({"username": username}))
def fetch_row_data_collection7(row_id):
    return collection7.find_one({"_id": ObjectId(row_id)})
def update_data_collection7(row_id, new_data):
    try:
        update_result = collection7.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
# def fetch_all_data_collection8(username):
#     return list(collection8.find({"username": username}))
# def fetch_row_data_collection8(row_id):
#     return collection8.find_one({"_id": ObjectId(row_id)})
# def update_data_collection8(row_id, new_data):
#     try:
#         update_result = collection8.find_one_and_update(
#             {"_id": ObjectId(row_id)},
#             {"$set": new_data},
#             return_document=True
#         )
#         return update_result is not None
#     except Exception as e:
#         st.error(f"Error updating data: {e}")
#         return False
def fetch_all_data_collection10(username):
    return list(collection10.find({"username": username}))
def fetch_row_data_collection10(row_id):
    return collection10.find_one({"_id": ObjectId(row_id)})
def update_data_collection10(row_id, new_data):
    try:
        update_result = collection10.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection11(username):
    return list(collection11.find({"username": username}))
def fetch_row_data_collection11(row_id):
    return collection11.find_one({"_id": ObjectId(row_id)})
def update_data_collection11(row_id, new_data):
    try:
        update_result = collection11.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection12(username):
    return list(collection12.find({"username": username}))
def fetch_row_data_collection12(row_id):
    return collection12.find_one({"_id": ObjectId(row_id)})
def update_data_collection12(row_id, new_data):
    try:
        update_result = collection12.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
# Function to display form for collection1
def display_form_collection1(row_data=None, row_id=None):
    st.header("Theory Courses Handled")

    Subject = st.text_input("Subject", value=row_data["subject"] if row_data else "", placeholder="Enter Your Subject")
    dep = st.text_input("Department", value=row_data["department"] if row_data else "", placeholder="Department Name")
    section = st.text_input("Class & Section", value=row_data["section"] if row_data else "", placeholder="Enter Classname & Section || Example: 3 CSE B")
    cp = st.text_input("Classes Planned", value=row_data["classes_planned"] if row_data else "", placeholder="No. Of Classes Planned")
    ch = st.text_input("Classes Held", value=row_data["classes_held"] if row_data else "", placeholder="No. Of Classes Held")
    option1 = st.selectbox(
        "Student Feedback (Cycle 1)",
        ("Excellent", "Good", "Satisfactory"),
        index=["Excellent", "Good", "Satisfactory"].index(row_data["feedback1"]) if row_data else 0
    )
    option2 = st.selectbox(
        "Student Feedback (Cycle 2)",
        ("Excellent", "Good", "Satisfactory"),
        index=["Excellent", "Good", "Satisfactory"].index(row_data["feedback2"]) if row_data else 0
    )
    res = st.text_input("Result Of Students", value=row_data["result"] if row_data else "", placeholder="% Of Students Passed")

    if st.button("Submit"):
        if not (Subject and dep and section and cp and ch and res):
            st.error("Please fill out all fields.")
            return

        try:
            points = calpoints(option1, option2, res)
            new_data = {
                "username": st.session_state.username,
                "subject": Subject,
                "department": dep,
                "section": section,
                "classes_planned": cp,
                "classes_held": ch,
                "feedback1": option1,
                "feedback2": option2,
                "result": res,
                "points": points,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection1(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection1.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Function to display form for collection4
def display_form_collection4(row_data=None, row_id=None):
    st.header("Learning Material")

    Subject = st.text_input("Material Developed for Subject", value=row_data["subject"] if row_data else "", placeholder="Enter Your Subject")
    year = st.text_input("Year", value=row_data["year"] if row_data else "", placeholder="Enter the Year")
    dep = st.text_input("Department", value=row_data["department"] if row_data else "", placeholder="Department Name")

    material_options = [
        "ICT Based teaching Material",
        "Interactive Courses/Online Courses",
        "Participatory Learning Modules/Teaching Notes"
    ]
    typem = st.selectbox(
        "Type of Material Developed",
        options=material_options,
        index=material_options.index(row_data["type_of_material"]) if row_data else 0
    )
    involvement_options = ["Single", "More than one"]
    option1 = st.selectbox(
        "Type of Involvement",
        options=involvement_options,
        index=involvement_options.index(row_data["type_of_involvement"]) if row_data else 0
    )

    if st.button("Submit"):
        if not (Subject and year and dep):
            st.error("Please fill out all fields.")
            return

        try:
            points = get_points_l4(typem, option1)
            new_data = {
                "username": st.session_state.username,
                "subject": Subject,
                "year": year,
                "department": dep,
                "type_of_material": typem,
                "type_of_involvement": option1,
                "points": points,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection4(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection4.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection5(row_data=None, row_id=None):
        st.title("Certificate Courses Done")
        certificate_options = [
            "Certificate course/Online certificate/MOOCs course offered by Foreign Universities",
            "Certificate course/Online certificate/MOOCs course offered by IIT/NIT",
            "Certificate course/Online certificate/MOOCs course offered by lower than IIT/NIT institutes or universities"
        ]
        
        certificate_type = st.selectbox(
            "Type of Certificate",index=certificate_options.index(row_data["certificate_type"]) if row_data else 0,
            options=certificate_options,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        relevance_options = ["Yes","No"]
        relevance = st.selectbox(
            "Is the Subject Relevant to Your Field",
            options=relevance_options,index=relevance_options.index(row_data["relevance"]) if row_data else 0,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        
        certificate_file = st.file_uploader("Upload Your Certificate PDF", type=["pdf"])
        if st.button("Submit"):
            if not (certificate_type and relevance and certificate_file):
                st.error("Please fill out all fields.")
                return

            try:
                user_data = collection_users.find_one({"username": st.session_state.username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                points = get_points_l5(certificate_type, relevance)
                certificate_content = certificate_file.read()
                encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')
                new_data = {
                    "username": st.session_state.username,
                    "certificate_type": certificate_type,
                    "relevance": relevance,
                    "points": points,  # Add points to the data
                    "department": department,
                    "date": datetime.datetime.now(),
                    "certificate_file": encoded_certificate
                }
                if row_id:
                    if update_data_collection5(row_id, new_data):
                        st.success("Data updated successfully!")
                        del st.session_state.current_row_id
                        del st.session_state.current_data
                    else:
                        st.error("Failed to update data.")
                else:
                    collection5.insert_one(new_data)
                    st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
def display_form_collection6(row_data=None, row_id=None):
    st.header("FDPs Attended")

    Subject = st.text_input("Name of the FDP", value=row_data["fdp_name"] if row_data else "", placeholder="Enter FDP Name")
    title = st.text_input("Title of Event", value=row_data["event_title"] if row_data else "", placeholder="Enter Event Title")
    ht = st.text_input("Host Institution", value=row_data["host_institution"] if row_data else "", placeholder="Enter Host Institution")
    
    # Dates
    frod = st.date_input("FDP Started Date", value=datetime.datetime.strptime(row_data["start_date"], "%Y-%m-%d") if row_data else datetime.datetime.now(), format="MM.DD.YYYY")
    tod = st.date_input("FDP Ended Date", value=datetime.datetime.strptime(row_data["end_date"], "%Y-%m-%d") if row_data else datetime.datetime.now(), format="MM.DD.YYYY")
    
    days = st.text_input("No of Days", value=row_data["no_of_days"] if row_data else "", placeholder="Enter Event No of Days")
    
    # Level of Institute
    level_options = ["IIT", "NIT", "University", "College"]
    level_of_institute = st.selectbox(
        "Level of Institute",
        options=level_options,
        index=level_options.index(row_data["institute_level"]) if row_data else 0
    )
    
    # Duration of the FDP
    duration_options = [">=2W", "1W-2W", "<1W"]
    fdp_duration = st.selectbox(
        "Duration of the FDP",
        options=duration_options,
        index=duration_options.index(row_data["fdp_duration"]) if row_data else 0
    )
    
    certificate_file = st.file_uploader("Upload Your FDP Certificate PDF", type=["pdf"])

    if st.button("Submit"):
        if not (Subject and title and ht and days):
            st.error("Please fill out all fields.")
            return

        if not certificate_file:
            st.error("Please upload your FDP certificate PDF.")
            return

        try:
            points = get_points_l6(level_of_institute, fdp_duration)
            user_data = collection_users.find_one({"username": st.session_state.username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return
            
            # Read the file content and encode it in base64
            certificate_content = certificate_file.read()
            encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')

            new_data = {
                "username": st.session_state.username,
                "fdp_name": Subject,
                "event_title": title,
                "host_institution": ht,
                "start_date": frod.strftime("%Y-%m-%d"),
                "end_date": tod.strftime("%Y-%m-%d"),
                "no_of_days": days,
                "institute_level": level_of_institute,
                "fdp_duration": fdp_duration,
                "points": points,
                "department": department,
                "date": datetime.datetime.now(),
                "certificate_file": encoded_certificate
            }
            
            if row_id:
                update_result = collection6.find_one_and_update(
                    {"_id": ObjectId(row_id)},
                    {"$set": new_data},
                    return_document=True
                )
                if update_result:
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection6.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection7(row_data=None, row_id=None):
    st.title("FDPs Organized")
    
    fdp_types = ["International (>=2W)", "National (>=2W)", "International (1W to 2W)", 
                 "National (1W to 2W)", "International (<1W)", "National (<1W)"]
    funding_types = ["External", "Sponsor", "Internal"]
    capacities = ["Convenor", "Co-convenor", "Sponsor", "Internal"]
    
    fdp_type = st.selectbox("Type of FDP", options=fdp_types, index=fdp_types.index(row_data["fdp_type"]) if row_data else 0)
    funding_type = st.selectbox("Type of Funding", options=funding_types, index=funding_types.index(row_data["funding_type"]) if row_data else 0)
    capacity = st.selectbox("Organised in the Capacity of", options=capacities, index=capacities.index(row_data["capacity_organised"]) if row_data else 0)
    
    frod = st.date_input("FDP STARTED DATE", value=datetime.datetime.strptime(row_data["start_date"], "%Y-%m-%d") if row_data else datetime.datetime.now(), format="MM.DD.YYYY")
    tod = st.date_input("FDP END DATE", value=datetime.datetime.strptime(row_data["end_date"], "%Y-%m-%d") if row_data else datetime.datetime.now(), format="MM.DD.YYYY")
    
    
    
    if st.button("Submit"):
        if not (fdp_type and funding_type and capacity):
            st.error("Please fill out all fields.")
            return
        try:
            points = get_points_l7(fdp_type, funding_type,capacity)
            user_data = collection_users.find_one({"username": st.session_state.username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return
            new_data = {
                "fdp_type": fdp_type,
                "funding_type": funding_type,
                "capacity_organised": capacity,
                "start_date": frod.strftime("%Y-%m-%d"),
                "end_date": tod.strftime("%Y-%m-%d"),
                "department":department,
                "points":points
            }
        
            if row_id:
                success = update_data_collection7(row_id, new_data)
                if success:
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection7.insert_one(new_data)
                st.success("Data added successfully!")
        except Exception as e:
            st.error(f"An error occured: {e}")

def display_form_collection10(row_data=None, row_id=None):
    st.header("MEMBERSHIPS WITH PROFESSIONAL BODIES")

    professional_body = st.text_input("Professional Body", value=row_data["professional_body"] if row_data else "", placeholder="Enter Professional Body Name")
    since_date = st.date_input("Since Date", value=datetime.datetime.strptime(row_data["since_date"], "%Y-%m-%d") if row_data else datetime.datetime.now())
    membership_type = st.selectbox("National/International", ["", "International Membership", "National Membership"],
                                   index=["", "International Membership", "National Membership"].index(row_data["membership_type"]) if row_data else 0)
    
    certificate_file = st.file_uploader("Upload your role certificate PDF", type=["pdf"])

    if st.button("Submit"):
        if not (professional_body and since_date and membership_type and certificate_file):
            st.error("Please fill out all required fields.")
            return
        
        if not certificate_file and not row_data:
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

            if certificate_file:
                # Read the file content and encode it in base64
                certificate_content = certificate_file.read()
                encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')
            else:
                encoded_certificate = row_data["certificate_file"]

            points = get_points_l10(membership_type)

            new_data = {
                "username": username,
                "professional_body": professional_body,
                "since_date": since_date.strftime("%Y-%m-%d"),
                "membership_type": membership_type,
                "points": points,
                "department": department,
                "certificate_file": encoded_certificate,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection10(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection10.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection11(row_data=None, row_id=None):
    st.header("Chairing Sessions & Delivering Talks and Lectures")

    # Inputs for form fields
    lec = st.text_input("Lectures", value=row_data["lectures"] if row_data else "", placeholder="Enter Lectures")
    dtalk = st.text_input("Delivering Talks", value=row_data["delivering_talks"] if row_data else "", placeholder="Enter Delivering Talks")
    ctalks = st.text_input("Chairing Talks", value=row_data["chairing_talks"] if row_data else "", placeholder="Enter Chairing Talks")

    Subject = st.selectbox("Geographical Level of platform of delivery", [
        "", "Chaired or Co-chaired (International)", "Chaired or Co-chaired (National)", 
        "Delivering talks & Lectures (International)", "Delivering talks & Lectures (National IIT/NIT Level)", 
        "Delivering talks & Lectures (University Level)", "Delivering talks & Lectures (College Level)"
    ], index=[
        "", "Chaired or Co-chaired (International)", "Chaired or Co-chaired (National)", 
        "Delivering talks & Lectures (International)", "Delivering talks & Lectures (National IIT/NIT Level)", 
        "Delivering talks & Lectures (University Level)", "Delivering talks & Lectures (College Level)"
    ].index(row_data["geographical_level"]) if row_data else 0)

    Subject3 = st.text_input("Inside or out campus", value=row_data["inside_or_out_campus"] if row_data else "", placeholder="Enter Inside or Out Campus")
    Subject1 = st.text_input("Name of the platform", value=row_data["platform_name"] if row_data else "", placeholder="Enter Platform Name")
    Subject4 = st.text_input("Type of delivery", value=row_data["delivery_type"] if row_data else "", placeholder="Enter Type of Delivery")

    Subject11 = st.text_input("Host institution details", value=row_data["host_institution_details"] if row_data else "", placeholder="Enter Host Institution Details")
    Subject13 = st.text_input("Who are the audience", value=row_data["audience_details"] if row_data else "", placeholder="Enter Audience Details")
    Subject21 = st.text_input("Type of guest or expert lecture delivered", value=row_data["guest_lecture_delivery_type"] if row_data else "", placeholder="Enter Type of Delivery")

    # File uploader for PDF
    file_uploader = st.file_uploader("Upload your all work in PDF", type=["pdf"])

    if st.button("Submit"):
        if not (lec and dtalk and ctalks and Subject and Subject3 and Subject1 and Subject4 and Subject11 and Subject13 and Subject21):
            st.error("Please fill out all required fields.")
            return
        
        if not file_uploader and not row_data:
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

            if file_uploader:
                # Read the file content and encode it in base64
                file_content = file_uploader.read()
                encoded_file = base64.b64encode(file_content).decode('utf-8')
            else:
                encoded_file = row_data["certificate_pdf"] if row_data else ""

            points = get_points_l11(Subject)

            new_data = {
                "username": username,
                "lectures": lec,
                "delivering_talks": dtalk,
                "chairing_talks": ctalks,
                "geographical_level": Subject,
                "inside_or_out_campus": Subject3,
                "platform_name": Subject1,
                "delivery_type": Subject4,
                "host_institution_details": Subject11,
                "audience_details": Subject13,
                "guest_lecture_delivery_type": Subject21,
                "certificate_pdf": encoded_file,
                "department": department,
                "points": points,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection11(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection11.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection12(row_data=None, row_id=None):
    st.header("Journal Publications and Guest Lectures")

    # Journal Publication Details
    st.subheader("Journal Publication Details")
    ath = st.text_input("No of authors", value=row_data["number_of_authors"] if row_data else "", placeholder="Enter Number of Authors")
    pat = st.text_input("Position of authorship", value=row_data["position_of_authorship"] if row_data else "", placeholder="Enter Position of Authorship")
    pubd = st.text_input("Publication details", value=row_data["publication_details"] if row_data else "", placeholder="Enter Publication Details")
    
    journal_options = [
        "SCI or equivalent", 
        "UGC referred Journals", 
        "Other International Journals", 
        "Other National Journals"
    ]
    Jtype = st.selectbox("Journal type", options=journal_options, index=journal_options.index(row_data["journal_type"]) if row_data else 0)
    
    # File uploader for PDF
    pdf_uploader1 = st.file_uploader("Upload your journal publication work in PDF", type=["pdf"], key="pdf1")

    # Guest Lecture Details
    st.subheader("Guest or Expert Lecture Details")
    Subject11 = st.text_input("Host institution details", value=row_data["host_institution_details"] if row_data else "", placeholder="Enter Host Institution Details")
    Subject13 = st.text_input("Who are the audience", value=row_data["audience_details"] if row_data else "", placeholder="Enter Audience Details")
    Subject21 = st.text_input("Type of delivery", value=row_data["guest_lecture_delivery_type"] if row_data else "", placeholder="Enter Type of Delivery")
    
    # File uploader for lecture PDF
    pdf_uploader2 = st.file_uploader("Upload your lecture work in PDF", type=["pdf"], key="pdf2")

    if st.button("Submit"):
        if not (ath and pat and pubd and Jtype and Subject11 and Subject13 and Subject21):
            st.error("Please fill out all required fields.")
            return

        if not pdf_uploader1 or not pdf_uploader2:
            st.error("Please upload both PDFs.")
            return
        
        try:
            username = st.session_state.username
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return
            points = get_points_l12(Jtype, "1st author" if pat.lower() == "1st" else "other")
            if pdf_uploader1:
                # Read the file content and encode it in base64
                file_content = pdf_uploader1.read()
                encoded_pdf1 = base64.b64encode(file_content).decode('utf-8')
            else:
                encoded_pdf1 = row_data["certificate_pdf"] if row_data else ""
            if pdf_uploader2:
                # Read the file content and encode it in base64
                file_content = pdf_uploader2.read()
                encoded_pdf2 = base64.b64encode(file_content).decode('utf-8')
            else:
                encoded_pdf2 = row_data["certificate_pdf"] if row_data else ""
            
            new_data = {
                "username": username,
                "number_of_authors": ath,
                "position_of_authorship": pat,
                "publication_details": pubd,
                "journal_type": Jtype,
                "journal_pdf": encoded_pdf1,
                "host_institution_details": Subject11,
                "audience_details": Subject13,
                "guest_lecture_delivery_type": Subject21,
                "lecture_pdf": encoded_pdf2,
                "department": department,
                "points": points,
                "date": datetime.datetime.now()
            }
            
            if row_id:
                if update_data_collection12(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection12.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
# Main function to display the app
def main(username):
    st.sidebar.title("Navigation")
    st.sidebar.write("Select a collection to manage:")

    collection_choice = st.sidebar.selectbox(
        "Select Collection",
        [
            "Theory Courses Handled",
            "Learning Material",
            "Certificates Courses Done",
            "FDPs Attended",
            "FDPs Organized",
            "Memberships with Professional Bodies",
            "Chairing Sessions & Delivering Talks and Lectures",
            "Journal Publications"  # Assuming l12 corresponds to Research Projects or similar
        ]
    )

    if collection_choice == "Theory Courses Handled":
        st.header("Theory Courses Handled")

        st.subheader("All Entries")
        if username:
            data_l1 = fetch_all_data_collection1(username)
            if data_l1:
                for entry in data_l1:
                    st.markdown(f"**Subject:** {entry['subject']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Class & Section:** {entry['section']}")
                    st.markdown(f"**Classes Planned:** {entry['classes_planned']}")
                    st.markdown(f"**Classes Held:** {entry['classes_held']}")
                    st.markdown(f"**Feedback (Cycle 1):** {entry['feedback1']}")
                    st.markdown(f"**Feedback (Cycle 2):** {entry['feedback2']}")
                    st.markdown(f"**Result:** {entry['result']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---") 
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection1(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)

    elif collection_choice == "Learning Material":
        st.header("Learning Material")

        st.subheader("All Entries")
        username_input = st.text_input("Enter Username", value=st.session_state.get("username", ""))
        if username_input:
            data_l4 = fetch_all_data_collection4(username_input)
            if data_l4:
                for entry in data_l4:
                    st.markdown(f"**Material for Subject:** {entry['subject']}")
                    st.markdown(f"**Year:** {entry['year']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Type of Material:** {entry['type_of_material']}")
                    st.markdown(f"**Involvement Type:** {entry['type_of_involvement']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---") 
            else:
                st.write("No data found")
        if 'current_row_id' in st.session_state:
            display_form_collection4(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)

    elif collection_choice == "Certificates Courses Done":
        st.header("Certificates Courses Done")

        st.subheader("All Entries")
        if username:
            data_l5 = fetch_all_data_collection5(username)
            if data_l5:
                for entry in data_l5:
                    st.markdown(f"**Certificate Type:** {entry['certificate_type']}")
                    st.markdown(f"**Relevance:** {entry['relevance']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---") 
            else:
                st.write("No data found")
        if 'current_row_id' in st.session_state:
            display_form_collection5(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)

    elif collection_choice == "FDPs Attended":
        st.header("FDPs Attended")

        st.subheader("All Entries")
        if username:
            data_l6 = fetch_all_data_collection6(username)
            if data_l6:
                for entry in data_l6:
                    st.markdown(f"**FDP Name:** {entry['fdp_name']}")
                    st.markdown(f"**Event Title:** {entry['event_title']}")
                    st.markdown(f"**Host Institution:** {entry['host_institution']}")
                    st.markdown(f"**Start Date:** {entry['start_date']}")
                    st.markdown(f"**End Date:** {entry['end_date']}")
                    st.markdown(f"**No of Days:** {entry['no_of_days']}")
                    st.markdown(f"**Institute Level:** {entry['institute_level']}")
                    st.markdown(f"**FDP Duration:** {entry['fdp_duration']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---")
            else:
                st.write("No data found")

        if 'current_row_id' in st.session_state:
            display_form_collection6(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)

    elif collection_choice == "FDPs Organized":
        st.header("FDPs Organized")

        st.subheader("All Entries")
        if username:
            data_l7 = fetch_all_data_collection7(username)
            if data_l7:
                for entry in data_l7:
                    st.markdown(f"**FDP Type:** {entry['fdp_type']}")
                    st.markdown(f"**Funding Type:** {entry['funding_type']}")
                    st.markdown(f"**Organized in the Capacity of:** {entry['capacity_organised']}")
                    st.markdown(f"**Start Date:** {entry['start_date']}")
                    st.markdown(f"**End Date:** {entry['end_date']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---")
            else:
                st.write("No data found")
        if 'current_row_id' in st.session_state:
            display_form_collection7(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)

    elif collection_choice == "Memberships with Professional Bodies":
        st.header("Memberships with Professional Bodies")

        st.subheader("All Entries")
        username_input = st.text_input("Enter Username", value=st.session_state.get("username", ""))
        if username_input:
            data_l10 = fetch_all_data_collection10(username_input)
            if data_l10:
                for entry in data_l10:
                    st.markdown(f"**Professional Body:** {entry['professional_body']}")
                    st.markdown(f"**Since Date:** {entry['since_date']}")
                    st.markdown(f"**Membership Type:** {entry['membership_type']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---") 
            else:
                st.write("No data found")
        if 'current_row_id' in st.session_state:
            display_form_collection10(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Chairing Sessions & Delivering Talks and Lectures":
        st.header("Chairing Sessions & Delivering Talks and Lectures")

        st.subheader("All Entries")
        username_input = st.text_input("Enter Username", value=st.session_state.get("username", ""))
        if username_input:
            data_l11 = fetch_all_data_collection11(username_input)
            if data_l11:
                for entry in data_l11:
                    st.markdown(f"**Lectures:** {entry['lectures']}")
                    st.markdown(f"**Delivering Talks:** {entry['delivering_talks']}")
                    st.markdown(f"**Chairing Talks:** {entry['chairing_talks']}")
                    st.markdown(f"**Geographical Level:** {entry['geographical_level']}")
                    st.markdown(f"**Inside or Out Campus:** {entry['inside_or_out_campus']}")
                    st.markdown(f"**Platform Name:** {entry['platform_name']}")
                    st.markdown(f"**Type of Delivery:** {entry['delivery_type']}")
                    st.markdown(f"**Host Institution Details:** {entry['host_institution_details']}")
                    st.markdown(f"**Audience Details:** {entry['audience_details']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---")
            else:
                st.write("No data found")

        if 'current_row_id' in st.session_state:
            display_form_collection11(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Journal Publications":
        st.subheader("All Entries")
        username_input = st.text_input("Enter Username", value=st.session_state.get("username", ""))
        
        if username_input:
            data_l12 = fetch_all_data_collection12(username_input)
            if data_l12:
                for entry in data_l12:
                    st.markdown(f"**Number of Authors:** {entry['number_of_authors']}")
                    st.markdown(f"**Position of Authorship:** {entry['position_of_authorship']}")
                    st.markdown(f"**Publication Details:** {entry['publication_details']}")
                    st.markdown(f"**Journal Type:** {entry['journal_type']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.experimental_rerun()
                    st.write("---")
            else:
                st.write("No data found")
        
        if 'current_row_id' in st.session_state:
            display_form_collection12(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)

# Run the main function with a test username
if __name__ == "__main__":
    if st.session_state.username:
        main(st.session_state.username)
