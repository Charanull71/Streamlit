import streamlit as st
from pymongo import MongoClient
from PIL import Image
import io
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
faculty_collection = db['faculty']  # Replace 'faculty' with your desired collection name

# Predefined lists of southern Indian states and their cities, including Odisha
states = [
    "Andhra Pradesh", "Telangana", "Karnataka", "Kerala", "Tamil Nadu", "Odisha"
]

# Alphabetically sorted lists of cities
cities = {
    "Andhra Pradesh": sorted([
        "Anantapur", "Bhimavaram", "Chittoor", "Eluru", "Guntur", "Jangareddygudem",
        "Kadapa", "Kakinada", "Kakinada", "Nandyal", "Nellore", "Ongole", "Peddapalli",
        "Rajahmundry", "Srikakulam", "Tadepalligudem", "Tirupati", "Visakhapatnam"
    ]),
    "Telangana": sorted([
        "Adilabad", "Hyderabad", "Jagtial", "Jagtiyal", "Kamareddy", "Khammam",
        "Kothagudem", "Mahbubnagar", "Medak", "Nalgonda", "Nagarkurnool", "Nirmal",
        "Ramagundam", "Warangal", "Wanaparthy", "Medchal", "Suryapet", "Nizamabad"
    ]),
    "Karnataka": sorted([
        "Bagalkot", "Belagavi", "Bellary", "Bengaluru", "Bidar", "Chikkamagaluru",
        "Davangere", "Gulbarga", "Hassan", "Hospet", "Hubli", "Karwar", "Kolar",
        "Mandya", "Mangalore", "Mysuru", "Raichur", "Shimoga", "Tumkur", "Udupi",
        "Yadgir"
    ]),
    "Kerala": sorted([
        "Alappuzha", "Cherthala", "Ernakulam", "Idukki", "Kollam", "Kochi",
        "Kannur", "Kottayam", "Malappuram", "Muvattupuzha", "Nedumangad", "Palakkad",
        "Pathanamthitta", "Perinthalmanna", "Thiruvananthapuram", "Wayanad", "Kunnamkulam"
    ]),
    "Tamil Nadu": sorted([
        "Arakkonam", "Cuddalore", "Chennai", "Dindigul", "Erode", "Kancheepuram",
        "Karur", "Kumarapalayam", "Madurai", "Nagercoil", "Ramanathapuram", "Salem",
        "Tiruchirappalli", "Tirunelveli", "Tiruppur", "Vellore", "Chengalpattu", "Tiruvannamalai"
    ]),
    "Odisha": sorted([
        "Angul", "Balasore", "Bhubaneswar", "Boudh", "Cuttack", "Dhenkanal",
        "Ganjam", "Jharsuguda", "Kendrapara", "Koraput", "Malkangiri", "Nayagarh",
        "Puri", "Rayagada", "Rourkela", "Sambalpur", "Subarnapur", "Jajpur"
    ])
}

# Function to convert image to Base64
def convert_image_to_base64(image_file):
    if image_file is not None:
        img = Image.open(image_file)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return img_str
    return ""

# Function to handle image upload and display
def display_image(image_file):
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption='Uploaded Picture', use_column_width=True)
    else:
        st.text("No image uploaded")

def main():
    # if "username" not in st.session_state:
    #     st.error("User not logged in.")
    #     return

    username = st.session_state.username

    st.title("Faculty Profile Form")

    # Upload Picture
    st.sidebar.header("Upload Picture")
    image_file = st.sidebar.file_uploader("Choose a picture", type=["jpg", "png", "jpeg"])

    # Personal Details
    st.header("Personal Details")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        job_title = st.text_input("Position")
        email = st.text_input("Contact Email")
        phone_number = st.text_input("Contact Number")

    with col2:
        office = st.text_input("Office Location")
        gov_id = st.text_input("Government ID Card Number")

    # Address Details
    st.header("Address")
    address_col1, address_col2 = st.columns(2)

    with address_col1:
        state = st.selectbox("State/Province", states)
        city = st.selectbox("City", cities[state])
        street_address = st.text_input("Street Address")
        zip_code = st.text_input("ZIP/Postal Code")
        country = st.text_input("Country", "India")

    with address_col2:
        pass # Empty column to align with the other fields

    # Education
    st.header("Education")
    highest_degree = st.text_input("Highest Degree")
    institution = st.text_input("Institution")
    year_of_graduation = st.text_input("Year of Graduation")

    # Research Interests
    st.header("Research Interests")
    research_interests = st.text_area("Areas of Research")

    # Publications
    st.header("Publications")
    publications = st.text_area("List of Key Publications (one per line)")

    # Professional Experience
    st.header("Professional Experience")
    experience = st.text_area("Previous Positions (one per line)")

    # Courses Taught
    st.header("Courses Taught")
    courses = st.text_area("List of Courses (one per line)")

    # Awards and Honors
    st.header("Awards and Honors")
    awards = st.text_area("Awards and Recognitions (one per line)")

    # Professional Affiliations
    st.header("Professional Affiliations")
    affiliations = st.text_area("Memberships (one per line)")

    # Biography
    st.header("Biography")
    biography = st.text_area("Short Biography")

    # Display the uploaded image
    st.sidebar.subheader("Preview")
    display_image(image_file)

    # Submit Button
    if st.button("Submit"):
        # Validate fields
        if not (name and job_title and email and phone_number and office and gov_id and street_address and city and state and zip_code and country and highest_degree and institution and year_of_graduation):
            st.error("Please fill out all fields.")
        else:
            # Convert image to Base64
            image_base64 = convert_image_to_base64(image_file)
            
            # Prepare data to insert into MongoDB
            data = {
                "username": username,
                "name": name,
                "job_title": job_title,
                "email": email,
                "phone_number": phone_number,
                "office": office,
                "gov_id": gov_id,
                "address": {
                    "street_address": street_address,
                    "city": city,
                    "state": state,
                    "zip_code": zip_code,
                    "country": country
                },
                "education": {
                    "highest_degree": highest_degree,
                    "institution": institution,
                    "year_of_graduation": year_of_graduation
                },
                "research_interests": research_interests,
                "publications": publications.split('\n'),
                "professional_experience": experience.split('\n'),
                "courses_taught": courses.split('\n'),
                "awards": awards.split('\n'),
                "affiliations": affiliations.split('\n'),
                "biography": biography,
                "image_base64": image_base64  # Store the image as Base64
            }
            
            try:
                # Insert data into MongoDB
                faculty_collection.insert_one(data)
                st.success("Faculty profile submitted successfully!")
            except Exception as e:
                st.error(f"An error occurred while submitting the profile: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
