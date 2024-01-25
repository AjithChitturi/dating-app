# Dating App Dashboard

This is a dating app built on python using streamlit library that allows users to fetch and store user data, display 10 random users, and find and visualize the nearest 'x' users to a selected user on a map. The project includes functionality for data storage using SQLite, API integration for fetching random user data, and geographical calculations to determine the nearest users.

## Project Structure

- ***main.py:*** The main script containing the Streamlit app, user interaction, and button functionalities.
- ***map.py:*** Module responsible for displaying users on a folium map using Streamlit.
- ***database.py:*** Script for database operations, including the creation of the SQLite users table.
- ***api.py:*** Module handling API requests to fetch random user data and storing it in the SQLite database.

## Features

- Fetch and Store Users: Use the provided API to fetch a specified number of random users and store them in the SQLite database.
- Fetch 10 Random Users: Retrieve and display 10 random users from the stored database.
- Display Nearest Users on Map: Enter the UID of a user and the number of nearest users to display, then visualize them on a map.


## Database Structure

The SQLite database (user.db) consists of a 'users' table with columns for UID, email, first name, last name, gender, latitude, longitude, and datetime.


## Getting Started
Install the required packages:
- ```pip install -r requirements.txt```

Run the Streamlit app:
- ```python -m streamlit run main.py```


## How to Use
- Enter the number of users to scrape and click "Fetch and Store Users" to populate the database.
- Enter the UID of a user and the number of nearest users to display, then click "Get Selected User and Display Nearest Users" to visualize them on the map.
- Click "Fetch 10 Random Users" to display information about 10 randomly selected users.
- ***Note:*** Ensure that you have the required dependencies installed and the SQLite database is accessible for the app to function correctly.






