import streamlit as st
import sqlite3
import requests
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import datetime
from sqlalchemy import text

# Function to create the 'users' table
def create_users_table():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            latitude REAL,
            longitude REAL,
            run_id INTEGER,
            datetime TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch and store users
def fetch_and_store_users(num_users):
    api_url = 'https://randomuser.me/api/'
    response = requests.get(api_url, params={'results': num_users})
    
    if response.status_code == 200:
        data = response.json()
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(run_id) FROM users")
        max_run_id = cursor.fetchone()[0]
        if max_run_id is None:
            max_run_id = 0
        run_id = max_run_id + 1
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for user in data['results']:
            uid = user['login']['uuid']
            email = user['email']
            first_name = user['name']['first']
            last_name = user['name']['last']
            gender = user['gender']
            latitude = user['location']['coordinates']['latitude']
            longitude = user['location']['coordinates']['longitude']

            cursor.execute('''
                INSERT INTO users (uid, email, first_name, last_name, gender, latitude, longitude, run_id, datetime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (uid, email, first_name, last_name, gender, latitude, longitude, run_id, current_datetime))

        conn.commit()
        conn.close()
        st.success(f"Successfully fetched and stored {num_users} users!")
    else:
        st.error("Error fetching user data from the API.")

# Function to fetch 10 random users for display
def fetch_10_random_users():
    create_users_table()  
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT uid, first_name, last_name, email FROM users ORDER BY RANDOM() LIMIT 10")
    random_users = cursor.fetchall()
    conn.close()
    st.subheader("10 Random Users:")
    for user_id, first_name, last_name, email in random_users:
        st.write(f"UID: {user_id}, Name: {first_name} {last_name}, Email: {email}")

# Function to get nearest x users for a selected user
# Function to get nearest x users for a selected user
def get_nearest_users(selected_user_uid, x):
    query = """
        SELECT uid, first_name, last_name, email, latitude, longitude,
               2 * 6371 * ASIN(SQRT(
                   POWER(SIN(RADIANS(:lat - latitude) / 2), 2) +
                   COS(RADIANS(:lat)) * COS(RADIANS(latitude)) *
                   POWER(SIN(RADIANS(:lon - longitude) / 2), 2)
               )) AS distance
        FROM users
        WHERE uid != :selected_user_uid
        ORDER BY distance
        LIMIT :x
    """

    with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM users WHERE uid=?", (selected_user_uid,))
        selected_user_coords = cursor.fetchone()
        if selected_user_coords:
            result = cursor.execute(str(text(query)), {'lat': selected_user_coords[0], 'lon': selected_user_coords[1],
                                                       'selected_user_uid': selected_user_uid, 'x': x})
            nearest_users = result.fetchall()
            return nearest_users
        else:
            return []



# Function to display users on a map
def display_users_on_map(users):
    st.subheader("Map of Users:")

    if users and len(users[0]) >= 6:
        center_user = users[0]
        m = folium.Map(location=[center_user[4], center_user[5]], zoom_start=3)
        for user in users:
            folium.Marker([user[4], user[5]], popup=f"{user[1]} {user[2]} ({user[3]})").add_to(m)
        folium_static(m)
    else:
        st.warning("No users found. Fetch and store users first.")

# Streamlit app
def main():
    st.title("Dating App Dashboard")
    create_users_table()
    num_users = st.number_input("Enter the number of users to scrape:", min_value=1, value=10)

    if st.button("Fetch and Store Users", key="fetch_button"):
        fetch_and_store_users(num_users)

    if st.button("Fetch 10 Random Users", key="fetch_10_random_button"):
        fetch_10_random_users()

    selected_user_uid = st.text_input("Enter UID of the user you want to select:")
    num_nearest_users = st.number_input("Enter the number of nearest users to display:", min_value=1, value=5)

    if st.button("Get Selected User and Display Nearest Users", key="get_selected_user_button"):
        if selected_user_uid:
            nearest_users = get_nearest_users(selected_user_uid, num_nearest_users)
            display_users_on_map(nearest_users)
        else:
            st.warning("Please enter a valid UID.")

# Run the app
if __name__ == '__main__':
    main()
