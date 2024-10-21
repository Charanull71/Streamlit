import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

# Optimized collection groups
collections = {
    'l1': db['l1'],
    'l2_btech': db['l2_btech'],
    'l2_mtech': db['l2_mtech'],
    'l3': db['l3'],
    'l4': db['l4']
}  # Limiting the number of collections for quick analysis

# Optimization: Fetch specific fields only, limit number of records analyzed
def fetch_user_data(username):
    user_data = []
    for collection in collections.values():
        data = list(collection.find({"username": username}, {"points": 1, "skills": 1}))  # Fetch points and skills
        user_data.extend(data)
        if len(user_data) > 50:  # Limit to first 50 records
            break
    return user_data

# Optimization: Aggregate data within MongoDB for quick top performer analysis
def analyze_top_performers(department):
    performers = []
    for collection in collections.values():
        pipeline = [
            {"$match": {"department": department}},
            {"$group": {"_id": "$username", "total_points": {"$sum": "$points"}, "skills": {"$push": "$skills"}}},
            {"$sort": {"total_points": -1}},
            {"$limit": 10}
        ]
        data = list(collection.aggregate(pipeline))
        for record in data:
            performers.append({"username": record["_id"], "points": record["total_points"], "skills": record["skills"]})
    df = pd.DataFrame(performers).sort_values(by="points", ascending=False).reset_index(drop=True)
    return df

# Generate responses with optimized queries
def generate_chatbot_responses(username, department):
    st.write("### Chatbot Analysis")
    st.write("Analyzing your performance... This should take less than 30 seconds.")

    user_data = fetch_user_data(username)
    total_points = sum(record.get("points", 0) for record in user_data)
    num_records = len(user_data)

    top_performers = analyze_top_performers(department)

    # Display user position
    user_position = 1 + len([p for p in top_performers.itertuples() if p.points > total_points])
    st.write(f"**Your Position:** {user_position}")

    # Display results
    st.write("**Top 3 Performers:**")
    st.write(top_performers.head(3))

    # Lagging skills
    if num_records > 0:
        user_skills = set(user_data[0].get("skills", []))  # Assuming skills are in the first record
        lagging_fields = []
        for performer in top_performers.itertuples():
            for skill in performer.skills:
                if skill not in user_skills:
                    lagging_fields.append(skill)

        if lagging_fields:
            st.write("**Skills Lagging:**")
            st.write(", ".join(lagging_fields))
        else:
            st.write("You're already excelling in all skills!")

        # Areas for Improvement
        improvement_suggestions = {}
        for performer in top_performers.itertuples():
            for skill in performer.skills:
                if skill not in user_skills:
                    improvement_suggestions[skill] = improvement_suggestions.get(skill, 0) + 1

        if improvement_suggestions:
            st.write("**What to Improve:**")
            for skill, count in improvement_suggestions.items():
                st.write(f"{skill}: Needs improvement by {count} fields.")
        else:
            st.write("You're a top performer! No improvements needed.")

    st.write("**Achievement Comparison:**")
    st.write(f"Your total points are **{total_points}**.")

    st.write("**Steps to Top Performance:**")
    highest_points = top_performers['points'].max() if not top_performers.empty else 0
    if total_points < highest_points:
        required_points = highest_points - total_points
        st.write(f"Aim to gain at least **{required_points}** more points.")
    else:
        st.write("You're already a top performer!")

# Streamlit app function
def main(username):
    st.title("Employee Performance Analysis - AI Chatbot")
    username = username
    department = st.text_input("Enter your department:").strip().lower()

    if st.button("Analyze and Compare"):
        if username and department:
            generate_chatbot_responses(username, department)
        else:
            st.warning("Please enter both username and department.")

if __name__ == "__main__":
    main(st.session_state.username)