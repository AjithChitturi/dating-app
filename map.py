import folium
from streamlit_folium import folium_static
import streamlit as st

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
