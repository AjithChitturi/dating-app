import streamlit as st
from api import fetch_and_store_users, fetch_10_random_users, get_nearest_users
from map import display_users_on_map
from database import create_users_table

def main():
    st.title("Dating App Dashboard")
    create_users_table()
    num_users = st.number_input("Enter the number of users to scrape:")

    if st.button("Fetch and Store Users", key="fetch_button"):
        fetch_and_store_users(num_users)

    if st.button("Fetch 10 Random Users", key="fetch_10_random_button"):
        fetch_10_random_users()

    selected_user_uid = st.text_input("Enter UID of the user you want to select:")
    num_nearest_users = st.number_input("Enter the number of nearest users to display:")

    if st.button("Get Selected User and Display Nearest Users", key="get_selected_user_button"):
        if selected_user_uid:
            nearest_users = get_nearest_users(selected_user_uid, num_nearest_users)
            display_users_on_map(nearest_users)
        else:
            st.warning("Please enter a valid UID.")

if __name__ == '__main__':
    main()
