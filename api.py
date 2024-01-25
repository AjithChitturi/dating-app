import requests
import datetime
import streamlit as st
import sqlite3
from sqlalchemy import text
from database import create_users_table


def fetch_and_store_users(num_users):
    api_url = 'https://randomuser.me/api/'
    response = requests.get(api_url, params={'results': num_users})
    
    if response.status_code == 200:
        data = response.json()
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
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
                INSERT INTO users (uid, email, first_name, last_name, gender, latitude, longitude, datetime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (uid, email, first_name, last_name, gender, latitude, longitude, current_datetime))

        conn.commit()
        conn.close()
        st.success(f"Successfully fetched and stored {num_users} users!")
    else:
        st.error("Error fetching user data from the API.")

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
