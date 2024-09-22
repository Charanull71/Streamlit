import streamlit as st
import time
from pymongo import MongoClient
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from WTF import advanceButton
from plotly.subplots import make_subplots

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
# collection = db['l1']
collections = {
    'l1': db['l1'],
    'l2_btech': db['l2_btech'],
    'l2_mtech': db['l2_mtech'],
    'l3': db['l3'],
    'l4': db['l4'],
    'l5': db['l5'],
    # Add other collections as needed
}
collections2 = {
    'l6': db['l6'],
    'l7': db['l7'],
    'l8': db['l8'],
    'l9': db['l8'],
    # Add other collections as needed
}
collections3 = {
    'l10': db['l10'],
    'l11': db['l11'],
    'l12': db['l12'],
    'l13': db['l13'],
    # Add other collections as needed
}
collections4 = {
    'l14': db['l14'],
    'l15': db['l15'],
    'l16': db['l16'],
    'l17': db['l17'],
    # Add other collections as needed
}
collections5 = {
    'l18': db['l18'],
    'l19': db['l19'],
    'l20': db['l20'],
    'l21': db['l21'],
    'l22': db['l22'],
    # Add other collections as needed
}

# def plot_user_data(username):
#     # Retrieve data for the user
#     data = list(collection.find({"username": username}))

#     if not data:
#         st.warning(f"No data found for username '{username}'.")
#         return

#     # Calculate total points and number of records
#     total_points = sum(record.get("points", 0) for record in data)
#     num_records = len(data)

#     # Prepare data for plotting
#     user_data = [{
#         'username': username,
#         'total_points': total_points,
#         'num_records': num_records
#     }]

#     df = pd.DataFrame(user_data)
#     fig = px.bar(df, x='username', y=['total_points', 'num_records'], barmode='group', title="User Points and Records Analysis")
#     st.plotly_chart(fig)
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
def plot_user_data2(username):
    table_names = []
    total_points_list = []
    num_records_list = []

    # Collect data from collections
    for table_name, collection in collections2.items():
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
def plot_user_data3(username):
    table_names = []
    total_points_list = []
    num_records_list = []

    # Collect data from collections
    for table_name, collection in collections3.items():
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
def plot_user_data4(username):
    table_names = []
    total_points_list = []
    num_records_list = []

    # Collect data from collections
    for table_name, collection in collections4.items():
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
def plot_user_data5(username):
    table_names = []
    total_points_list = []
    num_records_list = []

    # Collect data from collections
    for table_name, collection in collections5.items():
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

def main(username):
    col1, col2 = st.columns(2)
    with col2:
        advanceButton.main()
    with col1:
        if st.button("Retrieve Data and Plot Graph"):
            plot_user_data(username)
            plot_user_data2(username)
            plot_user_data3(username)
            plot_user_data4(username)
            plot_user_data5(username)
if __name__ == "__main__":
     # Replace with dynamic username retrieval logic if available
    main(st.session_state.username)