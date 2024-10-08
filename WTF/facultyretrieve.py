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
collection2_btech = db['l2_btech']
collection2_mtech = db['l2_mtech']
collection3 = db['l3']
collection4 = db['l4']
collection5 = db['l5']
collection6 = db['l6']
collection7 = db['l7']
collection8 = db['l8']
collection9 = db['l9']
collection10 = db['l10']
collection11 = db['l11']
collection12 = db['l12']
collection13 = db['l13']
collection14 = db['l14']
collection15 = db['l15']
collection16 = db['l16']
collection17 = db['l17']
collection18 = db['l18']
collection19 = db['l19']
collection20 = db['l20']
collection21 = db['l21']
collection22 = db['l22']
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
def calculate_btech_points(grade):
    grade_points = {
        "O": 100,
        "A+": 90,
        "A": 80,
        "B+": 70,
        "B": 60,
        "C": 50,
        "P": 40,
        "F": 0
    }
    return grade_points.get(grade, 0)

def calculate_mtech_points(grade, publication):
    grade_points = {
        ("Excellent", "Scopus & above"): 100,
        ("Excellent", "Non Scopus"): 80,
        ("Good", "Scopus & above"): 90,
        ("Good", "Non Scopus"): 70,
        ("Satisfactory", "Scopus & above"): 80,
        ("Satisfactory", "Non Scopus"): 60
    }
    return grade_points.get((grade, publication), 0)
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
def calculate_training_points(activity_type, hours):
    activity_points = {
        "Modular Program/Technical training [coordinator]": 100,
        "Resource person": 50,
        "Bridge course/remedial/makeup": 50,
        "Tutorial classes": 20
    }
    return activity_points.get(activity_type, 0)
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
points_dict8 = {
    "Principal": 100,
    "Vice Principal": 100,
    "Dean": 90,
    "Assoc. Dean": 90,
    "HOD": 80,
    "College level section Incharge": 80,
    "BoS Incharge": 50,
    "Library Incharge": 50,
    "Project Co-Ordinator": 50,
    "Committee Membership": 5  # Updated to 5 points for each membership
}
points_dict9 = {
    "If student selected for MNC or GATE/GRE qualified or became entrepreneur or got Govt. Job": 5,
    "If student selected for selected for a company other than MNC": 4,
    "If student Promoted/Releived without any of the above": 3,
    "If student Discontined/Detained": 0
}
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
def get_points_l13(proceeding_type, venue_location, authorship_position, venue_level):
    points_dict = {
        "IEEE/Springer or equivalent": {
            "India": {
                "> University Level": {"1st author": 80, "other": 10},
                "University Level": {"1st author": 70, "other": 10},
                "College Level": {"1st author": 60, "other": 5}
            },
            "Abroad": {
                "> University Level": {"1st author": 100, "other": 20},
                "University Level": {"1st author": 90, "other": 20},
                "College Level": {"1st author": 80, "other": 10}
            }
        },
        "Other Conferences": {
            "India": {
                "> University Level": {"1st author": 40, "other": 5},
                "University Level": {"1st author": 30, "other": 5},
                "College Level": {"1st author": 20, "other": 5}
            },
            "Abroad": {
                "> University Level": {"1st author": 50, "other": 10},
                "University Level": {"1st author": 40, "other": 10},
                "College Level": {"1st author": 30, "other": 5}
            }
        }
    }

    return points_dict.get(proceeding_type, {}).get(venue_location, {}).get(venue_level, {}).get(authorship_position, 0)
def get_points_l14(guide_type, date_of_registration):
    current_date = datetime.datetime.now()
    duration = (current_date - date_of_registration).days / 365.25  # Convert duration to years

    if guide_type.lower() == "guide":
        if duration <= 1:
            return 100
        elif 1 < duration <= 2:
            return 75
        elif 2 < duration <= 3:
            return 50
        else:
            return 25
    elif guide_type.lower() == "co-guide":
        if duration <= 1:
            return 50
        elif 1 < duration <= 2:
            return 35
        elif 2 < duration <= 3:
            return 20
        else:
            return 0
    return 0
def get_points_l15(issn_isbn, position_of_authorship, publishing_house_level):
    is_international = "International" in publishing_house_level
    has_isbn = issn_isbn.strip().upper() == "YES"
    is_first_author = "1st" in position_of_authorship.lower()

    if is_international:
        if has_isbn:
            return 100 if is_first_author else 25
        else:
            return 50 if is_first_author else 10
    else:
        if has_isbn:
            return 75 if is_first_author else 10
        else:
            return 35 if is_first_author else 5
def get_points_l16(patent_type, patent_category):
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
def get_points_l17(position):
    POSITION_POINTS = {
        "Single": 100,
        "First or Principle person": 50,
        "Other Persons": 10
    }
    return POSITION_POINTS.get(position, 0)
def get_points_l18(position):
    POSITION_POINTS = {
    "Single": 100,
    "First or Principle person": 50,
    "Other Persons": 10
}
    return POSITION_POINTS.get(position, 0)
def get_points_l19(position):
    if position == "Single":
        return 100
    elif position == "First or Principal Person":
        return 50
    elif position == "Other Persons":
        return 10
    else:
        return 0
def get_points_l20(award_type):
    if award_type == "International":
        return 100
    elif award_type == "National":
        return 50
    elif award_type == "State Level":
        return 25
    elif award_type == "University Level":
        return 15
    else:
        return 0
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
def fetch_all_data_collection2_btech(username):
    return list(collection2_btech.find({"username": username}))

# Function to fetch row data from collection1
def fetch_row_data_collection2_btech(row_id):
    return collection2_btech.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection1
def update_data_collection2_btech(row_id, new_data):
    try:
        update_result = collection2_btech.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection2_mtech(username):
    return list(collection2_mtech.find({"username": username}))

# Function to fetch row data from collection1
def fetch_row_data_collection2_mtech(row_id):
    return collection2_mtech.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection1
def update_data_collection2_mtech(row_id, new_data):
    try:
        update_result = collection2_mtech.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection3(username):
    return list(collection3.find({"username": username}))

# Function to fetch row data from collection1
def fetch_row_data_collection3(row_id):
    return collection3.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection1
def update_data_collection3(row_id, new_data):
    try:
        update_result = collection3.find_one_and_update(
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
def fetch_all_data_collection8(username):
    return list(collection8.find({"username": username}))
def fetch_row_data_collection8(row_id):
    return collection8.find_one({"_id": ObjectId(row_id)})
def update_data_collection8(row_id, new_data):
    try:
        update_result = collection8.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection9(username):
    return list(collection9.find({"username": username}))
def fetch_row_data_collection9(row_id):
    return collection9.find_one({"_id": ObjectId(row_id)})
def update_data_collection9(row_id, new_data):
    try:
        update_result = collection8.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
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
def fetch_all_data_collection13(username):
    return list(collection13.find({"username": username}))
def fetch_row_data_collection13(row_id):
    return collection13.find_one({"_id": ObjectId(row_id)})
def update_data_collection13(row_id, new_data):
    try:
        update_result = collection13.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection14(username):
    return list(collection14.find({"username": username}))
def fetch_row_data_collection14(row_id):
    return collection14.find_one({"_id": ObjectId(row_id)})
def update_data_collection14(row_id, new_data):
    try:
        update_result = collection14.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection15(username):
    return list(collection15.find({"username": username}))
def fetch_row_data_collection15(row_id):
    return collection15.find_one({"_id": ObjectId(row_id)})
def update_data_collection15(row_id, new_data):
    try:
        update_result = collection15.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection16(username):
    return list(collection16.find({"username": username}))
def fetch_row_data_collection16(row_id):
    return collection16.find_one({"_id": ObjectId(row_id)})
def update_data_collection16(row_id, new_data):
    try:
        update_result = collection16.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection17(username):
    return list(collection17.find({"username": username}))
def fetch_row_data_collection17(row_id):
    return collection17.find_one({"_id": ObjectId(row_id)})
def update_data_collection17(row_id, new_data):
    try:
        update_result = collection17.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection18(username):
    return list(collection18.find({"username": username}))
def fetch_row_data_collection18(row_id):
    return collection18.find_one({"_id": ObjectId(row_id)})
def update_data_collection18(row_id, new_data):
    try:
        update_result = collection18.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection19(username):
    return list(collection19.find({"username": username}))
def fetch_row_data_collection19(row_id):
    return collection19.find_one({"_id": ObjectId(row_id)})
def update_data_collection19(row_id, new_data):
    try:
        update_result = collection19.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection20(username):
    return list(collection20.find({"username": username}))
def fetch_row_data_collection20(row_id):
    return collection20.find_one({"_id": ObjectId(row_id)})
def update_data_collection20(row_id, new_data):
    try:
        update_result = collection20.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection21(username):
    return list(collection21.find({"username": username}))
def fetch_row_data_collection21(row_id):
    return collection21.find_one({"_id": ObjectId(row_id)})
def update_data_collection21(row_id, new_data):
    try:
        update_result = collection21.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False
def fetch_all_data_collection22(username):
    return list(collection22.find({"username": username}))

# Function to fetch row data from collection4
def fetch_row_data_collection22(row_id):
    return collection22.find_one({"_id": ObjectId(row_id)})

# Function to update data in collection4
def update_data_collection22(row_id, new_data):
    try:
        update_result = collection22.find_one_and_update(
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
def display_form_collection2_btech(row_data=None, row_id=None):
    st.header("Student Project Works Undertaken")    
    st.header("B.Tech Projects")

    btech_reg_no = st.text_input(
        "B.Tech Student Register No.",
        value=row_data["reg_no"] if row_data else "",
        placeholder="Enter B.Tech Register No."
    )
    btech_submitted = st.radio(
        "B.Tech Project Submitted?",
        ["YES", "NO"],
        index=["YES", "NO"].index(row_data["submitted"]) if row_data else 0
    )
    btech_grade = st.selectbox(
        "B.Tech Project Grade",
        ["O", "A+", "A", "B+", "B", "C", "P", "F"],
        index=["O", "A+", "A", "B+", "B", "C", "P", "F"].index(row_data["grade"]) if row_data else 0
    )
    btech_published = st.radio(
        "B.Tech Project Research output is published?",
        ["YES", "NO"],
        index=["YES", "NO"].index(row_data["published"]) if row_data else 0
    )

   
    if st.form_submit_button("Submit"):
        if not btech_reg_no:
            st.error("Please fill out all fields.")
            return

        try:
            btech_points = calculate_btech_points(btech_grade)
            new_data = {
                "username": st.session_state.username,
                "project_type": "B.Tech",
                "reg_no": btech_reg_no,
                "submitted": btech_submitted,
                "grade": btech_grade,
                "published": btech_published,
                "points": btech_points,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection2_btech(row_id, new_data):
                    st.success("B.Tech project data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection2_btech.insert_one(new_data)
                st.success("B.Tech project data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection2_mtech(row_data=None, row_id=None):
        st.header("Student Project Works Undertaken")  
        st.header("M.Tech/MBA Projects")
    
        mtech_reg_no = st.text_input(
            "M.Tech/MBA Student Register No.",
            value=row_data["reg_no"] if row_data else "",
            placeholder="Enter M.Tech/MBA Register No."
        )
        mtech_program = st.selectbox(
            "M.Tech/MBA Program",
            ["M.Tech", "MBA"],
            index=["M.Tech", "MBA"].index(row_data["program"]) if row_data else 0
        )
        mtech_specialization = st.text_input(
            "M.Tech/MBA Specialisation/Dept",
            value=row_data["specialization"] if row_data else "",
            placeholder="Enter Specialisation/Dept"
        )
        mtech_grade = st.selectbox(
            "M.Tech/MBA Project Grade",
            ["Excellent", "Good", "Satisfactory"],
            index=["Excellent", "Good", "Satisfactory"].index(row_data["grade"]) if row_data else 0
        )
        mtech_publication = st.selectbox(
            "M.Tech/MBA Project Research output is published in:",
            ["Scopus & above", "Non Scopus"],
            index=["Scopus & above", "Non Scopus"].index(row_data["publication"]) if row_data else 0
        )

        
        if st.form_submit_button("Submit"):
            if not (mtech_reg_no and mtech_specialization):
                st.error("Please fill out all fields.")
                return

            try:
                mtech_points = calculate_mtech_points(mtech_grade, mtech_publication)
                new_data = {
                    "username": st.session_state.username,
                    "project_type": "M.Tech/MBA",
                    "reg_no": mtech_reg_no,
                    "program": mtech_program,
                    "specialization": mtech_specialization,
                    "grade": mtech_grade,
                    "publication": mtech_publication,
                    "points": mtech_points,
                    "date": datetime.datetime.now()
                }
                if row_id:
                    if update_data_collection2_mtech(row_id, new_data):
                        st.success("M.Tech/MBA project data updated successfully!")
                        del st.session_state.current_row_id
                        del st.session_state.current_data
                    else:
                        st.error("Failed to update data.")
                else:
                    collection2_mtech.insert_one(new_data)
                    st.success("M.Tech/MBA project data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
def display_form_collection3(row_data=None, row_id=None):
    st.header("Student Training Activities")
    st.subheader("Training Activity Details")
    activity_type = st.selectbox("Type of Activity", [
        "Modular Program/Technical training [coordinator]",
        "Resource person",
        "Bridge course/remedial/makeup",
        "Tutorial classes"
    ], index=[
        "Modular Program/Technical training [coordinator]",
        "Resource person",
        "Bridge course/remedial/makeup",
        "Tutorial classes"
    ].index(row_data["activity_type"]) if row_data else 0)
    
    year_program = st.text_input("Year & Program", value=row_data["year_program"] if row_data else "", placeholder="Enter Year & Program")
    dept_specialization = st.text_input("Dept./Specialisation", value=row_data["dept_specialization"] if row_data else "", placeholder="Enter Dept./Specialisation")
    period_from = st.date_input("From", value=row_data["period_from"].date() if row_data else datetime.date.today())
    period_to = st.date_input("To", value=row_data["period_to"].date() if row_data else datetime.date.today())
    hours = st.number_input("Hours", min_value=0, step=1, value=row_data["hours"] if row_data else 0)
    description = st.text_area("Brief description of program", value=row_data["description"] if row_data else "", placeholder="Enter description of the program")

    if st.button("Submit"):
        if not (activity_type and year_program and dept_specialization and hours and description):
            st.error("Please fill out all fields.")
            return

        try:
            training_points = calculate_training_points(activity_type, hours)

            new_data = {
                "username": st.session_state.username,
                "activity_type": activity_type,
                "year_program": year_program,
                "dept_specialization": dept_specialization,
                "period_from": datetime.datetime.combine(period_from, datetime.datetime.min.time()),
                "period_to": datetime.datetime.combine(period_to, datetime.datetime.min.time()),
                "hours": hours,
                "description": description,
                "points": training_points,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection3(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection3.insert_one(new_data)
                st.success("Training activity data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Assuming the update function is defined similarly to update_data_collection1 and update_data_collection2
def update_data_collection3(row_id, new_data):
    try:
        collection3.update_one({"_id": row_id}, {"$set": new_data})
        return True
    except Exception as e:
        st.error(f"An error occurred while updating: {e}")
        return False

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
        )
        relevance_options = ["Yes","No"]
        relevance = st.selectbox(
            "Is the Subject Relevant to Your Field",
            options=relevance_options,index=relevance_options.index(row_data["relevance"]) if row_data else 0,
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
def display_form_collection8(row_data=None, row_id=None):
    st.title("Professional Roles")

    # College level roles options
    college_roles = ["None", "Principal", "Vice Principal", "Dean", "Assoc. Dean"]
    department_roles = ["None", "HOD", "College level section Incharge"]
    
    # Fetching user details
    user_data = collection_users.find_one({"username": st.session_state.username})
    if user_data:
        department = user_data.get("department", "")
    else:
        st.error("Username not found in users collection.")
        return

    # Form inputs for College level roles
    st.write("**College level (Principal, Vice Principal, Deans etc.)**")
    college_role = st.selectbox("Select College Level Role", options=college_roles, index=college_roles.index(row_data["college_role"]) if row_data else 0)
    
    if college_role != "None":
        college_role_nature_of_work = st.text_input("Nature of work", value=row_data["college_role_nature_of_work"] if row_data else "")
        college_role_since = st.date_input("Since Date", value=datetime.datetime.strptime(row_data["college_role_since"], "%Y-%m-%d") if row_data else datetime.datetime.now())
        college_role_till = st.date_input("Till Date", value=datetime.datetime.strptime(row_data["college_role_till"], "%Y-%m-%d") if row_data else datetime.datetime.now())
        st.write(f"**Points for {college_role}:** {points_dict8[college_role]}")
    else:
        college_role_nature_of_work = college_role_since = college_role_till = None

    # Form inputs for Department level roles
    st.write("**Department level (HOD, Incharge)**")
    department_role = st.selectbox("Select Department Level Role", options=department_roles, index=department_roles.index(row_data["department_role"]) if row_data else 0)
    
    if department_role != "None":
        department_name = st.text_input("Department", value=row_data["department_name"] if row_data else department)
        department_nature_of_work = st.text_input("Nature of work", value=row_data["department_nature_of_work"] if row_data else "")
        department_since = st.date_input("Since Date", value=datetime.datetime.strptime(row_data["department_since"], "%Y-%m-%d") if row_data else datetime.datetime.now())
        department_till = st.date_input("Till Date", value=datetime.datetime.strptime(row_data["department_till"], "%Y-%m-%d") if row_data else datetime.datetime.now())
        st.write(f"**Points for {department_role}:** {points_dict8[department_role]}")
    else:
        department_name = department_nature_of_work = department_since = department_till = None

    # Incharges and Committee Coordinators
    st.write("**Incharges & Committee Coordinators**")
    incharges_text = st.text_input("Enter roles (comma-separated)", value=", ".join(row_data["incharges"]) if row_data else "")
    incharges_points = len(incharges_text.split(",")) * 5 if incharges_text else 0
    st.write(f"**Total Points for Incharges:** {incharges_points}")

    # Committee Memberships
    st.write("**Committee Memberships**")
    memberships_text = st.text_input("Enter memberships (comma-separated)", value=", ".join(row_data["memberships"]) if row_data else "")
    memberships_points = len(memberships_text.split(",")) * 5 if memberships_text else 0
    st.write(f"**Total Points for Memberships:** {memberships_points}")

    # File uploader for certificate PDF
    certificate_file = st.file_uploader("Upload role certificates (PDF)", type=["pdf"])

    # On form submit
    if st.button("Submit"):
        if not (college_role != "None" or department_role != "None" or incharges_text or memberships_text):
            st.error("Please fill out at least one role.")
            return
        
        if not certificate_file:
            st.error("Please upload the certificate PDF.")
            return

        try:
            # Read and encode certificate
            certificate_content = certificate_file.read()
            encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')

            # Calculate total points
            total_points = 0
            if college_role != "None":
                total_points += points_dict8[college_role]
            if department_role != "None":
                total_points += points_dict8[department_role]
            total_points += incharges_points + memberships_points
            total_points = min(total_points, 100)

            # Data structure to insert/update
            new_data = {
                "college_role": college_role,
                "college_role_nature_of_work": college_role_nature_of_work,
                "college_role_since": college_role_since.strftime("%Y-%m-%d"),
                "college_role_till": college_role_till.strftime("%Y-%m-%d"),
                "department_role": department_role,
                "department_name": department_name,
                "department_nature_of_work": department_nature_of_work,
                "department_since": department_since.strftime("%Y-%m-%d"),
                "department_till": department_till.strftime("%Y-%m-%d"),
                "incharges": [role.strip() for role in incharges_text.split(",")],
                "memberships": [role.strip() for role in memberships_text.split(",")],
                "certificate_file": encoded_certificate,
                "total_points": total_points,
                "department": department,
                "date": datetime.datetime.now()
            }

            # Insert or update data
            if row_id:
                collection8.update_one({"_id": row_id}, {"$set": new_data})
                st.success("Data updated successfully!")
            else:
                collection8.insert_one(new_data)
                st.success("Data added successfully!")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
def get_btech_years():
    return ["1", "2", "3", "4"]

# Predefined departments
def get_departments():
    departments = ["CSE", "ECE", "EEE", "Mechanical", "Civil"]  # Add more departments as needed
    return departments

# Main function for displaying the form
def display_form_collection9(username, row_data=None):
    with st.form("l9"):
        st.title("Students Counselling/Mentoring")

        # Fetch user data from the 'users' collection
        user_data = collection_users.find_one({"username": username})
        if user_data:
            department = user_data.get("department", "")
        else:
            st.error("Username not found in users collection.")
            return

        # Dropdown for B.Tech year (numeric)
        year = st.selectbox("Select Year", get_btech_years(), index=get_btech_years().index(row_data["year"]) if row_data else 0)

        # Dropdown for Department
        department = st.selectbox("Select Department", get_departments(), index=get_departments().index(row_data["department"]) if row_data else 0)

        # Combine Year and Department into a single field for storage
        year_department = f"{year} - {department}"

        student_regd_nos = st.text_input("Regd. no(s). of student", value=row_data["student_regd_nos"] if row_data else "", placeholder="18A51A0501-18A51A0521")
        number_of_students = st.text_input("Number of students", value=row_data["number_of_students"] if row_data else "", placeholder="Enter number of students")
        specific_remarks = st.text_input("Specific remarks", value=row_data["specific_remarks"] if row_data else "", placeholder="Enter specific remarks (e.g., 16 Selected in Campus Interviews)")

        # Dropdown for student outcome
        student_outcome = st.selectbox(
            "Select student outcome",
            list(points_dict9.keys()),
            index=list(points_dict9.keys()).index(row_data["student_outcome"]) if row_data else 0
        )

        # Form submission
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not student_regd_nos or not number_of_students or not specific_remarks or not student_outcome:
                st.error("Please fill out all required fields.")
                return

            try:
                # Calculate points based on student outcome and number of students
                points = points_dict9[student_outcome] * int(number_of_students)

                # Structure of the data to insert or update
                data = {
                    "username": username,
                    "year_department": year_department,
                    "student_regd_nos": student_regd_nos,
                    "number_of_students": number_of_students,
                    "specific_remarks": specific_remarks,
                    "student_outcome": student_outcome,
                    "points": points,
                    "department": department,
                    "date": datetime.datetime.now()
                }

                if row_data:
                    collection9.update_one({"_id": row_data["_id"]}, {"$set": data})
                    st.success("Data updated successfully!")
                else:
                    collection9.insert_one(data)
                    st.success("Data inserted successfully!")

            except Exception as e:
                st.error(f"An error occurred: {e}")

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
def display_form_collection13(row_data=None, row_id=None):
    st.title("CONFERENCE PUBLICATIONS")

    st.write("Conference Publication Details")
    ath = st.text_input("No of authors", value=row_data["number_of_authors"] if row_data else "", placeholder="Enter Number of Authors", key="number_of_authors")
    pat = st.selectbox("Position of authorship", ["", "1st author", "other"], index=["", "1st author", "other"].index(row_data["position_of_authorship"]) if row_data else 0, key="position_of_authorship")
    pven = st.text_input("Venue of Conference", value=row_data["conference_venue"] if row_data else "", placeholder="Enter Conference Venue", key="conference_venue")
    Jtype = st.selectbox("Venue at India/Abroad", ["", "India", "Abroad"], index=["", "India", "Abroad"].index(row_data["venue_location"]) if row_data else 0, key="venue_location")
    ptype = st.selectbox("Proceedings type", ["", "IEEE/Springer or equivalent", "Other Conferences"], index=["", "IEEE/Springer or equivalent", "Other Conferences"].index(row_data["proceedings_type"]) if row_data else 0, key="proceedings_type")
    venue_level = st.selectbox("Venue Level", ["", "> University Level", "University Level", "College Level"], index=["", "> University Level", "University Level", "College Level"].index(row_data["venue_level"]) if row_data else 0, key="venue_level")

    # File uploader for PDF
    pdf_uploader = st.file_uploader("Upload your work in PDF", type=["pdf"], key="pdf_uploader")
    if row_data and row_data.get("pdf"):
        st.write("Current PDF is uploaded.")
    
    if st.button("Submit"):
        # Check for empty fields
        if not (ath and pat and pven and Jtype and ptype and venue_level):
            st.error("Please fill out all required fields.")
            return

        if not pdf_uploader and not row_data.get("pdf"):
            st.error("Please upload the PDF.")
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
            pdf_content = pdf_uploader.read() if pdf_uploader else base64.b64decode(row_data["pdf"])
            encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

            # Calculate points
            points = get_points_l13(ptype, Jtype, pat, venue_level)

            new_data = {
                "username": username,
                "number_of_authors": ath,
                "position_of_authorship": pat,
                "conference_venue": pven,
                "venue_location": Jtype,
                "proceedings_type": ptype,
                "venue_level": venue_level,
                "pdf": encoded_pdf,
                "department": department,
                "points": points,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection13(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection13.insert_one(new_data)
                st.success(f"Data inserted successfully! Total Points: {points}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection14(row_data=None, row_id=None):
    st.header("RESEARCH GUIDANCE (Ph.D/M.Phil)")

    n1 = st.text_input("No. Of STUDENTS Completed Ph.D/M.Phil:", value=row_data["students_completed"] if row_data else "", placeholder="Enter number of students completed")
    deg = st.text_input("Degree", value=row_data["degree"] if row_data else "", placeholder="Enter Degree")
    uni = st.text_input("University", value=row_data["university"] if row_data else "", placeholder="Enter University")
    gui = st.selectbox("Guide/Co-Guide", ["", "Guide", "Co-Guide"], index=["", "Guide", "Co-Guide"].index(row_data["guide"]) if row_data else 0)
    frod3 = st.date_input("Date of Registration", row_data["date_of_registration"] if row_data else datetime.datetime.now().date(), format="YYYY-MM-DD")
    stype = st.text_input("Student Particulars", value=row_data["student_particulars"] if row_data else "", placeholder="Enter Particulars Of Student")

    if st.button("Submit"):
        # Check for empty fields
        if not (n1 and deg and uni and gui and stype):
            st.error("Please fill out all required fields.")
            return

        try:
            # Convert date to datetime.datetime
            frod3 = datetime.datetime.combine(frod3, datetime.datetime.min.time())
            username = st.session_state.username  # Replace with your actual way of getting username

            # Query users collection to get department for the specified username
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return

            # Calculate points
            points = get_points_l14(gui, frod3)

            data = {
                "username": username,
                "students_completed": n1,
                "degree": deg,
                "university": uni,
                "guide": gui,
                "date_of_registration": frod3,
                "student_particulars": stype,
                "department": department,
                "points": points,
                "date": datetime.datetime.now()
            }

            if row_id:
                if collection14.update_one({"_id": row_id}, {"$set": data}):
                    st.success(f"Data updated successfully!")
                else:
                    st.error("Failed to update data.")
            else:
                collection14.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection15(row_data=None, row_id=None):
    st.header("BOOK PUBLICATIONS")

    n1 = st.text_input("No. Of Books Published up to the previous assessment year:", value=row_data["books_published_previous"] if row_data else "", placeholder="Enter number of books published")
    aut = st.text_input("No of authors", value=row_data["authors"] if row_data else "", placeholder="Enter Number of Authors")
    pos = st.selectbox("Position of authorship", ["1st author", "Co-author", "Other author"], index=["1st author", "Co-author", "Other author"].index(row_data["position_of_authorship"]) if row_data else 0)
    iss = st.selectbox("ISSN/ISBN No.", ["", "YES", "NO"], index=["", "YES", "NO"].index(row_data["issn_isbn"]) if row_data else 0)
    lph = st.selectbox("Level of Publishing House", ["International Publisher", "National Publisher"], index=["International Publisher", "National Publisher"].index(row_data["publishing_house_level"]) if row_data else 0)
    tpb = st.text_input("Title and other particulars of the book", value=row_data["book_particulars"] if row_data else "", placeholder="Enter Title and other particulars of the book")

    if st.button("Submit"):
        # Check for empty fields
        if not (n1 and aut and pos and iss and lph and tpb):
            st.error("Please fill out all required fields.")
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

            # Calculate points
            points = get_points_l15(iss, pos, lph)

            new_data = {
                "username": username,
                "books_published_previous": n1,
                "authors": aut,
                "position_of_authorship": pos,
                "issn_isbn": iss,
                "publishing_house_level": lph,
                "book_particulars": tpb,
                "department": department,
                "points": points,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection15(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection15.insert_one(new_data)
                st.success(f"Data inserted successfully! Total Points: {points}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection16(row_data=None, row_id=None):
    st.title("PATENTS")

    with st.form("l16"):
        # Section for patents filed/obtained up to previous assessment year
        st.subheader("No. Of PATENTS Filed/Obtained up to previous assessment year")
        n1 = st.text_input("No. Of PATENTS Filed:", value=row_data.get("patents_filed_previous", "") if row_data else "", placeholder="Enter number of patents filed up to previous assessment year")
        n2 = st.text_input("No. Of PATENTS Obtained:", value=row_data.get("patents_obtained_previous", "") if row_data else "", placeholder="Enter number of patents obtained up to previous assessment year")

        # Section for patents filed/obtained in present assessment year
        st.subheader("PATENTS Published in present assessment year")
        status_of_patent = st.selectbox("Status of Patent", ["", "Filed", "Obtained"], index=["", "Filed", "Obtained"].index(row_data.get("status_of_patent", "")) if row_data else 0)
        level_of_patent = st.selectbox("Level of Patent", ["", "International", "National", "State", "Local"], index=["", "International", "National", "State", "Local"].index(row_data.get("filed_type", "")) if row_data else 0)
        date_of_filing = st.date_input("Date of Filing", value=row_data.get("date_of_registration", datetime.datetime.now().date()) if row_data else datetime.datetime.now().date(), format="YYYY-MM-DD")
        description_of_patent = st.text_area("Description of Patent", value=row_data.get("description_of_patent", "") if row_data else "", placeholder="Enter description of the patent")

        points = get_points_l16(status_of_patent, level_of_patent) if status_of_patent and level_of_patent else 0


        submit_button = st.form_submit_button("Submit")
        if submit_button:
            # Check for empty fields
            if not (n1 and n2 and status_of_patent and level_of_patent and description_of_patent):
                st.error("Please fill out all required fields.")
                return

            try:
                # Convert date to datetime.datetime
                date_of_filing = datetime.datetime.combine(date_of_filing, datetime.datetime.min.time())

                username = st.session_state.username  # Replace with your actual way of getting username
                
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return

                new_data = {
                    "username": username,
                    "patents_filed_previous": n1,
                    "patents_obtained_previous": n2,
                    "status_of_patent": status_of_patent,
                    "level_of_patent": level_of_patent,  # Adjusted based on the original code
                    "date_of_registration": date_of_filing,
                    "description_of_patent": description_of_patent,
                    "department": department,
                    "points":points,
                    "date": datetime.datetime.now()
                }

                if row_id:
                    # Assuming `update_data_collection16` function exists for updating
                    if update_data_collection16(row_id, new_data):
                        st.success("Data updated successfully!")
                        del st.session_state.current_row_id
                        del st.session_state.current_data
                    else:
                        st.error("Failed to update data.")
                else:
                    collection16.insert_one(new_data)
                    st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
def display_form_collection17(row_data=None, row_id=None):
    st.header("PRODUCT DESIGN / SOFTWARE DEVELOPMENT")

    n1 = st.text_input("No. Of Products designed/developed up to previous assessment year:", value=row_data["products_previous"] if row_data else "", key="products_previous")
    
    st.write("No. Of Products designed/developed up to present assessment year:")
    nop = st.text_input("Name of Product / SW", value=row_data["product_name"] if row_data else "", placeholder="Enter Name of Product / SW", key="product_name")
    
    nof = st.text_input("No. Of Faculty in the team work", value=row_data["faculty_count"] if row_data else "", placeholder="Enter No. Of Faculty in the team work", key="faculty_count")
    
    # Dropdown for position in the team
    pos = st.selectbox("Position in the team", options=["Single", "First or Principle person", "Other Persons"], index=["Single", "First or Principle person", "Other Persons"].index(row_data["position_in_team"]) if row_data else 0, key="position_in_team")
    pos_points = get_points_l17(pos)
    
    dop = st.text_input("Description of the product / SW", value=row_data["product_description"] if row_data else "", placeholder="Enter Description of the product / SW", key="product_description")

    # Display points
    st.write(f"Points for Position in Team: {pos} - {pos_points}")

    if st.button("Submit"):
        # Check for empty fields
        if not (n1 and nop and nof and dop):
            st.error("Please fill out all required fields.")
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
            
            new_data = {
                "username": username,
                "products_previous": n1,
                "product_name": nop,
                "faculty_count": nof,
                "position_in_team": pos,
                "position_points": pos_points,
                "product_description": dop,
                "department": department,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection17(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection17.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection18(row_data=None, row_id=None):
    st.header("CONSULTANCY")
    
    total_consultancy_previous = st.text_input("Total Consultancy upto previous assessment year: (in Rs.)", value=row_data["total_consultancy_previous"] if row_data else "", key="total_consultancy_previous")
    
    st.write("Consultancy in present assessment year:")
    toc = st.text_input("Title of Consultancy work", value=row_data["title_consultancy_work"] if row_data else "", placeholder="Enter Title of Consultancy work", key="title_consultancy_work")
    
    nga = st.text_input("Name of Granting Agency", value=row_data["granting_agency"] if row_data else "", placeholder="Name of Granting Agency", key="granting_agency")
    
    nci = st.text_input("No of Coordinators involved", value=row_data["coordinators_involved"] if row_data else "", placeholder="Enter No of Coordinators involved", key="coordinators_involved")
    
    # Dropdown for position in the team
    poc = st.selectbox("Position in order of coordinatorship", options=["Single", "First or Principle person", "Other Persons"], index=["Single", "First or Principle person", "Other Persons"].index(row_data["position_coordinatorship"]) if row_data else 0, key="position_coordinatorship")
    poc_points = get_points_l18(poc)
    
    sin = st.date_input(
        "Since:",
        value=row_data["since_date"] if row_data else datetime.date.today(),
        format="MM.DD.YYYY",
        key="since_date"
    )
    
    gm = st.text_input("Grant/Amount mobilised", value=row_data["grant_amount_mobilised"] if row_data else "", placeholder="Enter Grant/Amount mobilised", key="grant_amount_mobilised")

    if st.button("Submit"):
        # Check for empty fields
        if not (total_consultancy_previous and toc and nga and nci and gm):
            st.error("Please fill out all required fields.")
            return
        
        try:
            # Convert date to datetime.datetime
            sin = datetime.datetime.combine(sin, datetime.datetime.min.time())
            username = st.session_state.username  # Replace with your actual way of getting username
            
            # Query users collection to get department for the specified username
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return
            
            new_data = {
                "username": username,
                "total_consultancy_previous": total_consultancy_previous,
                "title_consultancy_work": toc,
                "granting_agency": nga,
                "coordinators_involved": nci,
                "position_coordinatorship": poc,
                "position_points": poc_points,
                "since_date": sin,
                "grant_amount_mobilised": gm,
                "department": department,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection18(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection18.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection19(row_data=None, row_id=None):
    st.header("Funded Projects")

    title = st.text_input("Title of Project", value=row_data["title"] if row_data else "", placeholder="Enter Title")
    position = st.selectbox(
        "Position in the team",
        ("Single", "First or Principal Person", "Other Persons"),
        index=["Single", "First or Principal Person", "Other Persons"].index(row_data["position"]) if row_data else 0
    )
    funded_by = st.text_input("Funded by", value=row_data["funded_by"] if row_data else "", placeholder="Enter Funding Source")
    period_from = st.date_input("Period From", value=datetime.datetime.strptime(row_data["period_from"], '%Y-%m-%d') if row_data else datetime.date.today())
    period_to = st.date_input("Period To", value=datetime.datetime.strptime(row_data["period_to"], '%Y-%m-%d') if row_data else datetime.date.today())
    grant_amount = st.text_input("Grant/Amount Mobilised", value=row_data["grant_amount"] if row_data else "", placeholder="Enter Amount")
    pi_option = st.selectbox(
        "Are you PI?",
        ("Yes", "No"),
        index=["Yes", "No"].index(row_data["pi_option"]) if row_data else 0
    )

    if st.button("Submit"):
        if not (title and funded_by and period_from and period_to and grant_amount):
            st.error("Please fill out all fields.")
            return

        try:
            points = get_points_l19(position)
            username = st.session_state.username  # Replace with your actual way of getting username

            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            else:
                st.error("Username not found in users collection.")
                return

            new_data = {
                "username": username,
                "department": department,
                "title": title,
                "position": position,
                "funded_by": funded_by,
                "period_from": period_from.strftime('%Y-%m-%d'),
                "period_to": period_to.strftime('%Y-%m-%d'),
                "grant_amount": grant_amount,
                "pi_option": pi_option,
                "points": points,
                "date": datetime.datetime.now()
            }

            if row_id:
                if update_data_collection19(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection19.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection20(row_data=None, row_id=None):
    st.header("FELLOWSHIP/AWARD")
    award_name = st.text_input("Fellowship/Award Name", value=row_data["award_name"] if row_data else "", key="award_name")
    award_type = st.selectbox("Fellowship/Award Type", ("International", "National", "State Level", "University Level"), index=["International", "National", "State Level", "University Level"].index(row_data["award_type"]) if row_data else 0, key="award_type")
    points = get_points_l20(award_type)

    if st.button("Submit Award"):
        if not (award_name and award_type):
            st.error("Please fill out all fields.")
            return

        try:
            username = st.session_state.username  # Replace with your actual way of getting username

                # Query users collection to get department for the specified username
            user_data = collection_users.find_one({"username": username})
            if user_data:
                department = user_data.get("department", "")
            new_data = {
                "username":st.session_state.username,
                "department":department,
                "award_name": award_name,
                "award_type": award_type,
                "points": points,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection20(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection20.insert_one(new_data)
                st.success("Fellowship/Award data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection21(row_data=None, row_id=None):
    st.header("Ph.D. Details")
    st.subheader("Please fill out the following details:")

    phd_holder = st.radio("Are you a Ph.D. holder?", ("YES", "NO"), index=["YES", "NO"].index(row_data["phd_holder"]) if row_data else 1)
    
    year_of_registration = None
    if phd_holder == "NO":
        year_of_registration = st.number_input("Year of registration for pursuing Ph.D.", min_value=1900, max_value=datetime.datetime.now().year, step=1, value=row_data["year_of_registration"] if row_data else datetime.datetime.now().year)

    course_files_submitted = st.radio("Have you submitted 'Course files of all subjects' up to current month?", ("YES", "NO"), index=["YES", "NO"].index(row_data["course_files_submitted"]) if row_data else 1)
    
    reason_files_not_submitted = None
    if course_files_submitted == "NO":
        reason_files_not_submitted = st.text_area("Reason for not submitting Course files of all subjects", value=row_data["reason_files_not_submitted"] if row_data else "")

    course_attainment_completed = st.radio("Have you completed 'Course attainment' of all subjects up to current month?", ("YES", "NO"), index=["YES", "NO"].index(row_data["course_attainment_completed"]) if row_data else 1)
    
    reason_course_attainment_not_completed = None
    if course_attainment_completed == "NO":
        reason_course_attainment_not_completed = st.text_area("Reason for not completing Course attainment of all subjects", value=row_data["reason_course_attainment_not_completed"] if row_data else "")

    if st.button("Submit"):
        if phd_holder == "NO" and not year_of_registration:
            st.error("Please fill out all fields.")
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
            new_data = {
                "username":st.session_state.username,
                "department":department,
                "phd_holder": phd_holder,
                "year_of_registration": year_of_registration,
                "course_files_submitted": course_files_submitted,
                "reason_files_not_submitted": reason_files_not_submitted if course_files_submitted == "NO" else None,
                "course_attainment_completed": course_attainment_completed,
                "reason_course_attainment_not_completed": reason_course_attainment_not_completed if course_attainment_completed == "NO" else None,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection21(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection21.insert_one(new_data)
                st.success("Ph.D. details inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
def display_form_collection22(row_data=None, row_id=None):
    st.header("LEAVES AVAILED")

    if row_data and 'from_date' in row_data and 'to_date' in row_data:
        from_date = datetime.datetime.strptime(row_data["from_date"], '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(row_data["to_date"], '%Y-%m-%d').date()
    else:
        from_date = datetime.date.today()
        to_date = datetime.date.today()

    from_date = st.date_input("From Date", value=from_date)
    to_date = st.date_input("To Date", value=to_date)

    classes = st.number_input("Cls", min_value=0, step=1, value=row_data["classes"] if row_data else 0)
    hp_classes = st.number_input("HP Cls", min_value=0, step=1, value=row_data["hp_classes"] if row_data else 0)
    c_classes = st.number_input("C Cls", min_value=0, step=1, value=row_data["c_classes"] if row_data else 0)
    ods = st.number_input("ODs", min_value=0, step=1, value=row_data["ods"] if row_data else 0)
    study_leaves = st.number_input("Study leaves", min_value=0, step=1, value=row_data["study_leaves"] if row_data else 0)
    academic_leaves = st.number_input("Academic leaves", min_value=0, step=1, value=row_data["academic_leaves"] if row_data else 0)
    permissions = st.number_input("No. of permissions", min_value=0, step=1, value=row_data["permissions"] if row_data else 0)
    other_leaves_remarks = st.text_area("Any other leaves & remarks", value=row_data["other_leaves_remarks"] if row_data else "", placeholder="Enter any other leaves & remarks")

    if st.button("Submit"):
        if not (from_date and to_date):
            st.error("Please fill out all fields.")
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
            new_data = {
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
                "other_leaves_remarks": other_leaves_remarks,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data_collection22(row_id, new_data):
                    st.success("Data updated successfully!")
                    del st.session_state.current_row_id
                    del st.session_state.current_data
                else:
                    st.error("Failed to update data.")
            else:
                collection22.insert_one(new_data)
                st.success("Leaves availed data inserted successfully!")
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
            "Student Project Works Undertaken",
            "Student Training Activities",
            "Learning Material",
            "Certificates Courses Done",
            "FDPs Attended",
            "FDPs Organized",
            "Professional Roles",
            "Student Counselling/Monitoring",
            "Memberships with Professional Bodies",
            "Chairing Sessions & Delivering Talks and Lectures",
            "Journal Publications",
            "Conference Publications",
            "Research Guidance",
            "Book Publications",
            "Patents",
            "Product Design/Software Development",
            "Consultancy",
            "Funded Projects",
            "Fellowship/Award",
            "Ph.D. Details",
            "Leaves Availed"  # Adding this new collection
        ]
    )
    if 'project_type' not in st.session_state:
        st.session_state.project_type = "B.Tech" 

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
                        st.rerun()
                    st.write("---") 
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection1(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Student Project Works Undertaken":
        st.header("Student Project Works Undertaken")
        st.subheader("All Entries")

        if username:
            # Fetch B.Tech and M.Tech/MBA data
            data_l2_btech = fetch_all_data_collection2_btech(username)
            data_l2_mtech = fetch_all_data_collection2_mtech(username)

            # Display B.Tech projects
            if data_l2_btech:
                for entry in data_l2_btech:
                    st.markdown(f"**Project Type:** {entry['project_type']}")
                    st.markdown(f"**Register No.:** {entry['reg_no']}")
                    st.markdown(f"**Submitted:** {entry.get('submitted', 'N/A')}")
                    st.markdown(f"**Grade:** {entry['grade']}")
                    st.markdown(f"**Published:** {entry['published']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_btech_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.session_state.project_type = "B.Tech"  # Set project type
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found for B.Tech projects.")

            # Display M.Tech/MBA projects
            if data_l2_mtech:
                for entry in data_l2_mtech:
                    st.markdown(f"**Project Type:** {entry['project_type']}")
                    st.markdown(f"**Register No.:** {entry['reg_no']}")
                    st.markdown(f"**Program:** {entry['program']}")
                    st.markdown(f"**Specialization:** {entry['specialization']}")
                    st.markdown(f"**Grade:** {entry['grade']}")
                    st.markdown(f"**Published:** {entry['publication']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_mtech_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.session_state.project_type = "M.Tech/MBA"  # Set project type
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found for M.Tech/MBA projects.")

        # Display form for editing or creating new entries
        if 'current_row_id' in st.session_state:
            with st.form(key='project_form'):
                if st.session_state.project_type == "B.Tech":
                    display_form_collection2_btech(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
                elif st.session_state.project_type == "M.Tech/MBA":
                    display_form_collection2_mtech(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Student Training Activities":
        st.header("Student Training Activities")

        st.subheader("All Entries")
        if username:
            data_l3 = fetch_all_data_collection3(username)
            if data_l3:
                for entry in data_l3:
                    st.markdown(f"**Type of Activity:** {entry['activity_type']}")
                    st.markdown(f"**Year & Program:** {entry['year_program']}")
                    st.markdown(f"**Dept./Specialisation:** {entry['dept_specialization']}")
                    st.markdown(f"**Period From:** {entry['period_from']}")
                    st.markdown(f"**Period To:** {entry['period_to']}")
                    st.markdown(f"**Hours:** {entry['hours']}")
                    st.markdown(f"**Description:** {entry['description']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---") 
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection3(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Learning Material":
        st.header("Learning Material")

        st.subheader("All Entries")
        if username:
            data_l4 = fetch_all_data_collection4(username)
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
                        st.rerun()
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
                        st.rerun()
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
                        st.rerun()
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
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found")
        if 'current_row_id' in st.session_state:
            display_form_collection7(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "FDPs Organized":
        st.title("Professional Roles")

    if username:
        data = collection8.find({"username": username})
        if data:
            for entry in data:
                # Display College Level Roles
                st.markdown(f"**College Role:** {entry.get('college_role', 'N/A')}")
                st.markdown(f"**Nature of Work (College):** {entry.get('college_role_nature_of_work', 'N/A')}")
                st.markdown(f"**Since Date (College):** {entry.get('college_role_since', 'N/A')}")
                st.markdown(f"**Till Date (College):** {entry.get('college_role_till', 'N/A')}")
                st.markdown(f"**Points (College):** {points_dict8.get(entry.get('college_role', 'None'), 0)}")

                # Display Department Level Roles
                st.markdown(f"**Department Role:** {entry.get('department_role', 'N/A')}")
                st.markdown(f"**Department Name:** {entry.get('department_name', 'N/A')}")
                st.markdown(f"**Nature of Work (Department):** {entry.get('department_nature_of_work', 'N/A')}")
                st.markdown(f"**Since Date (Department):** {entry.get('department_since', 'N/A')}")
                st.markdown(f"**Till Date (Department):** {entry.get('department_till', 'N/A')}")
                st.markdown(f"**Points (Department):** {points_dict8.get(entry.get('department_role', 'None'), 0)}")

                # Modify Button
                if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                    st.session_state.current_row_id = str(entry["_id"])
                    st.session_state.current_data = entry
                    st.rerun()
                st.write("---")
        else:
            st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection8(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
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
                        st.rerun()
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
                        st.rerun()
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
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found")
        
        if 'current_row_id' in st.session_state:
            display_form_collection12(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Conference Publications":
        st.header("Conference Publications")

        st.subheader("All Entries")
        username_input = st.text_input("Enter Username", value=st.session_state.get("username", ""))
        
        if username_input:
            data_l13 = fetch_all_data_collection13(username_input)
            if data_l13:
                for entry in data_l13:
                    st.markdown(f"**Proceeding Type:** {entry['proceedings_type']}")
                    st.markdown(f"**Number of Authors:** {entry['number_of_authors']}")
                    st.markdown(f"**Authorship Position:** {entry['position_of_authorship']}")
                    st.markdown(f"**Conference Venue:** {entry['conference_venue']}")
                    st.markdown(f"**Venue Location:** {entry['venue_location']}")
                    st.markdown(f"**Venue Level:** {entry['venue_level']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found")
        
        if 'current_row_id' in st.session_state:
            display_form_collection13(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Research Guidance":
        st.header("Research Guidance")
        st.subheader("All Entries")
        username_input = st.text_input("Enter Username", value=st.session_state.get("username", ""),disabled=True)
        if username_input:
            data_l14 = fetch_all_data_collection14(username_input)
            if data_l14:
                for entry in data_l14:
                    st.markdown(f"**Number of Students:** {entry['students_completed']}")
                    st.markdown(f"**Degree:** {entry['degree']}")
                    st.markdown(f"**University:** {entry['university']}")
                    st.markdown(f"**Guide Type:** {entry['guide']}")
                    st.markdown(f"**Date of Registration:** {entry['date_of_registration']}")
                    st.markdown(f"**Student Particulars:** {entry['student_particulars']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
               st.write("No data found")
        if 'current_row_id' in st.session_state:
            display_form_collection14(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Book Publications":
        st.header("Book Publications")

        st.subheader("All Entries")
        if username:
            data_l15 = fetch_all_data_collection15(username)
            if data_l15:
                for entry in data_l15:
                    st.markdown(f"**Books Published up to previous assessment year:** {entry['books_published_previous']}")
                    st.markdown(f"**Number of Authors:** {entry['authors']}")
                    st.markdown(f"**Position of Authorship:** {entry['position_of_authorship']}")
                    st.markdown(f"**ISSN/ISBN No.:** {entry['issn_isbn']}")
                    st.markdown(f"**Level of Publishing House:** {entry['publishing_house_level']}")
                    st.markdown(f"**Title and other particulars of the book:** {entry['book_particulars']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found.")

        if st.sidebar.button("Add New Entry"):
            st.session_state.current_row_id = None
            st.session_state.current_data = None
            st.rerun()

        if 'current_row_id' in st.session_state:
            display_form_collection15(st.session_state.current_data, st.session_state.current_row_id)
    elif collection_choice == "Patents":
        st.header("Patents")

        st.subheader("All Entries")
        if username:
            data_l16 = fetch_all_data_collection16(username)
            if data_l16:
                for entry in data_l16:
                    st.markdown(f"**Patents Filed (Previous Year):** {entry['patents_filed_previous']}")
                    st.markdown(f"**Patents Obtained (Previous Year):** {entry['patents_obtained_previous']}")
                    st.markdown(f"**Status of Patent:** {entry['status_of_patent']}")
                    st.markdown(f"**Level of Patent:** {entry['level_of_patent']}")
                    st.markdown(f"**Date of Filing:** {entry['date_of_filing'].strftime('%Y-%m-%d')}")
                    st.markdown(f"**Description of Patent:** {entry['description_of_patent']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Date:** {entry['date'].strftime('%Y-%m-%d')}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---") 
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection16(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Product Design/Software Development":
        st.header("Product Design/Software Development")

        st.subheader("All Entries")
        if username:
            data_l17 = fetch_all_data_collection17(username)
            if data_l17:
                for entry in data_l17:
                    st.markdown(f"**No. Of Products designed/developed upto previous assessment year:** {entry['products_previous']}")
                    st.markdown(f"**Name of Product / SW:** {entry['product_name']}")
                    st.markdown(f"**No. Of Faculty in the team work:** {entry['faculty_count']}")
                    st.markdown(f"**Position in the team:** {entry['position_in_team']}")
                    st.markdown(f"**Points for Position:** {entry['position_points']}")
                    st.markdown(f"**Description of the product / SW:** {entry['product_description']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---") 
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection17(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Consultancy":
        st.header("Consultancy")

        st.subheader("All Entries")
        if username:
            data_l18 = fetch_all_data_collection18(username)
            if data_l18:
                for entry in data_l18:
                    st.markdown(f"**Total Consultancy up to previous assessment year:** {entry['total_consultancy_previous']}")
                    st.markdown(f"**Title of Consultancy Work:** {entry['title_consultancy_work']}")
                    st.markdown(f"**Granting Agency:** {entry['granting_agency']}")
                    st.markdown(f"**No of Coordinators Involved:** {entry['coordinators_involved']}")
                    st.markdown(f"**Position in order of Coordinatorship:** {entry['position_coordinatorship']}")
                    st.markdown(f"**Since Date:** {entry['since_date']}")
                    st.markdown(f"**Grant/Amount Mobilised:** {entry['grant_amount_mobilised']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Points:** {entry['position_points']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection18(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Funded Projects":
        st.subheader("All Entries")
        if username:
            data_l19 = collection19.find({"username": username})
            if data_l19:
                for entry in data_l19:
                    st.markdown(f"**Title:** {entry['title']}")
                    st.markdown(f"**Position:** {entry['position']}")
                    st.markdown(f"**Funded by:** {entry['funded_by']}")
                    st.markdown(f"**Period From:** {entry['period_from'].strftime('%Y-%m-%d')}")
                    st.markdown(f"**Period To:** {entry['period_to'].strftime('%Y-%m-%d')}")
                    st.markdown(f"**Grant Amount:** {entry['grant_amount']}")
                    st.markdown(f"**PI Option:** {entry['pi_option']}")
                    st.markdown(f"**Date:** {entry['date'].strftime('%Y-%m-%d')}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            # Assuming you have a similar form function for funded projects
            display_form_collection19(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Fellowship/Award":
        st.header("Fellowship/Award")

        st.subheader("All Entries")
        if username:
            data_l20 = fetch_all_data_collection20(username)
            if data_l20:
                for entry in data_l20:
                    st.markdown(f"**Award Name:** {entry['award_name']}")
                    st.markdown(f"**Award Type:** {entry['award_type']}")
                    st.markdown(f"**Points:** {entry['points']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection20(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Ph.D. Details":
        st.header("Ph.D. Details")

        st.subheader("All Entries")
        if username:
            data_l21 = fetch_all_data_collection21(username)
            if data_l21:
                for entry in data_l21:
                    st.markdown(f"**Ph.D. Holder:** {entry['phd_holder']}")
                    st.markdown(f"**Year of Registration:** {entry['year_of_registration']}")
                    st.markdown(f"**Course Files Submitted:** {entry['course_files_submitted']}")
                    st.markdown(f"**Reason Files Not Submitted:** {entry['reason_files_not_submitted']}")
                    st.markdown(f"**Course Attainment Completed:** {entry['course_attainment_completed']}")
                    st.markdown(f"**Reason Course Attainment Not Completed:** {entry['reason_course_attainment_not_completed']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection21(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)
    elif collection_choice == "Leaves Availed":
        st.header("Leaves Availed")

        st.subheader("All Entries")
        if username:
            data_l22 = fetch_all_data_collection22(username)
            if data_l22:
                for entry in data_l22:
                    st.markdown(f"**From Date:** {entry['from_date']}")
                    st.markdown(f"**To Date:** {entry['to_date']}")
                    st.markdown(f"**Cls:** {entry['classes']}")
                    st.markdown(f"**HP Cls:** {entry['hp_classes']}")
                    st.markdown(f"**C Cls:** {entry['c_classes']}")
                    st.markdown(f"**ODs:** {entry['ods']}")
                    st.markdown(f"**Study Leaves:** {entry['study_leaves']}")
                    st.markdown(f"**Academic Leaves:** {entry['academic_leaves']}")
                    st.markdown(f"**Permissions:** {entry['permissions']}")
                    st.markdown(f"**Other Leaves & Remarks:** {entry['other_leaves_remarks']}")
                    st.markdown(f"**Department:** {entry['department']}")
                    st.markdown(f"**Date:** {entry['date']}")
                    if st.button(f"Modify", key=f"modify_{entry['_id']}"):
                        st.session_state.current_row_id = str(entry["_id"])
                        st.session_state.current_data = entry
                        st.rerun()
                    st.write("---")
            else:
                st.write("No data found.")
        if 'current_row_id' in st.session_state:
            display_form_collection22(row_data=st.session_state.current_data, row_id=st.session_state.current_row_id)


# Run the main function with a test username
if __name__ == "__main__":
    if st.session_state.username:
        main(st.session_state.username)
