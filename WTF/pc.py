import streamlit as st
from pymongo import MongoClient
import pandas as pd
from WTF import advanceButton
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

collections = {
    'l1': db['l1'],
    'l2_btech': db['l2_btech'],
    'l2_mtech': db['l2_mtech'],
    'l3': db['l3'],
    'l4': db['l4'],
    'l5': db['l5'],
    'l6': db['l6'],
    'l7': db['l7'],
    'l8': db['l8'],
    'l9': db['l8'],
    'l10': db['l10'],
    'l11': db['l11'],
    'l12': db['l12'],
    'l13': db['l13'],
    'l14': db['l14'],
    'l15': db['l15'],
    'l16': db['l16'],
    'l17': db['l17'],
    'l18': db['l18'],
    'l19': db['l19'],
    'l20': db['l20'],
    'l21': db['l21'],
    'l22': db['l22'],
}

def get_user_info(username):
    users_collection = db['users']
    user = users_collection.find_one({"username": username})
    if user:
        return user.get("role", ""), user.get("department", "")
    return "", ""

def plot_user_data(username):
    table_names = []
    total_points_list = []
    num_records_list = []

    # Collect data from collections
    for table_name, collection in collections.items():
        data = list(collection.find({"username": username}))
        total_points = sum(record.get("points", 0) for record in data)
        num_records = len(data)

        table_names.append(table_name)
        total_points_list.append(total_points)
        num_records_list.append(num_records)

    # Create subplots with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add bar traces
    fig.add_trace(
        go.Bar(x=table_names, y=total_points_list, name="Total Points"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=table_names, y=num_records_list, name="Number of Records"),
        secondary_y=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Table Names")

    # Set y-axes titles
    fig.update_yaxes(title_text="Total Points", secondary_y=False)
    fig.update_yaxes(title_text="Number of Records", secondary_y=True, range=[0, 100])

    fig.update_layout(title_text="User Points and Records Analysis")

    st.plotly_chart(fig)

def plot_hod_data(department, selected_table):
    collection = collections[selected_table]
    data = list(collection.find({"department": {"$regex": f"^{department}$", "$options": "i"}}))

    if not data:
        st.warning(f"No data found for department '{department}' in table '{selected_table}'.")
        return

    usernames = []
    total_points_list = []
    num_records_list = []

    user_data = {}
    for record in data:
        username = record.get("username")
        points = record.get("points", 0)
        if username not in user_data:
            user_data[username] = {"total_points": 0, "num_records": 0}
        user_data[username]["total_points"] += points
        user_data[username]["num_records"] += 1

    for username, values in user_data.items():
        usernames.append(username)
        total_points_list.append(values["total_points"])
        num_records_list.append(values["num_records"])

    # Create subplots with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add line traces
    fig.add_trace(
        go.Scatter(x=usernames, y=total_points_list, name="Total Points", mode='lines+markers'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=usernames, y=num_records_list, name="Number of Records", mode='lines+markers'),
        secondary_y=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Usernames")

    # Set y-axes titles
    fig.update_yaxes(title_text="Total Points", secondary_y=False)
    fig.update_yaxes(title_text="Number of Records", secondary_y=True)

    fig.update_layout(title_text=f"Department {department} - User Points and Records Analysis ({selected_table})")

    st.plotly_chart(fig)

def main(username):
    # Retrieve current logged-in user's role and department
    col1, col2 = st.columns(2)
    with col2:
        advanceButton.main()
    with col1:
        role, department = get_user_info(username)

    

        if role == "HOD":
            selected_table = st.selectbox("Select Table", list(collections.keys()))
            plot_hod_data(department, selected_table)
        elif role == "Principal":
            dept_input = st.text_input("Enter Department").strip()
            if dept_input:
                plot_hod_data(dept_input, selected_table)
        else:
            plot_user_data(username)

# if __name__ == "__main__":
#     # Simulate logged-in user for demonstration; replace with actual session state management
#     main(st.session_state.username)
