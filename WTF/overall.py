import pymongo
import math
import streamlit as st

# MongoDB connection setup using your provided connection string and database
client = pymongo.MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

# Function to calculate the average for a specific section
def calculate_section_average(collections, username):
    total_sum = 0
    total_entries = 0

    # Loop through each collection in the section
    for collection_name in collections:
        collection = db[collection_name]
        # Retrieve all entries for the faculty (username)
        entries = collection.find({"username": username})
        
        # Loop through the entries and sum the points for each entry
        for entry in entries:
            # Debug print to inspect the entry (if needed)
            # print(f"Processing entry: {entry}")
            points = entry.get("points", 0)  # Use .get() to avoid KeyError, default to 0 if 'points' is missing
            
            # Check if points is None or not a number (to avoid adding invalid data)
            if points is None or not isinstance(points, (int, float)):
                # Handle invalid or missing 'points'
                points = 0

            total_sum += points
            total_entries += 1

    # Return the average points for the section, avoid division by zero
    if total_entries == 0:
        return 0
    return total_sum / total_entries

# Function to compute the final total for a faculty and store it in MongoDB
def main(username):
    # Sections divided into collections
    section1_collections = ['l1', 'l2', 'l3', 'l4', 'l5']
    section2_collections = ['l6', 'l7', 'l8', 'l9', 'l10', 'l11']
    section3_collections = ['l12', 'l13', 'l14', 'l15', 'l16', 'l17', 'l18', 'l19', 'l20']

    # Calculate the average for each section
    section1_average = calculate_section_average(section1_collections, username)
    section2_average = calculate_section_average(section2_collections, username)
    section3_average = calculate_section_average(section3_collections, username)

    # Sum up the points for each section and ceiling to 100
    section1_total = min(100, math.ceil(section1_average))
    section2_total = min(100, math.ceil(section2_average))
    section3_total = min(100, math.ceil(section3_average))

    # Sum of all three sections capped at a maximum of 300
    total_marks = section1_total + section2_total + section3_total
    total_marks = min(300, total_marks)

    # Display results on Streamlit
    st.write(f"### Section 1 (l1 to l5) Total Marks: {section1_total}")
    st.write(f"### Section 2 (l6 to l11) Total Marks: {section2_total}")
    st.write(f"### Section 3 (l12 to l20) Total Marks: {section3_total}")
    st.write(f"## Overall Total Marks: {total_marks}")

    # Store the result in MongoDB
    result = {
        "username": username,
        "section1_total": section1_total,
        "section2_total": section2_total,
        "section3_total": section3_total,
        "total_marks": total_marks
    }

    db["faculty_totals"].insert_one(result)
    st.success(f"Total marks for {username} successfully saved in the database.")


