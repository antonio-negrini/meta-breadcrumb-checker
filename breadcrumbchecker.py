import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd


st.title("Breadcrumb Microdata Checker")

# Create a radio button to select whether or not the site requires authorization
requires_auth = st.radio("Does the site require authorization?", ("Yes", "No"))

# Create text inputs for the username and password if the site requires authorization
if requires_auth == "Yes":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

# Create a text input for the URL to be checked
url = st.text_input("Enter URL")

# Define a function to check for breadcrumb microdata
def check_breadcrumb_microdata(url, auth=None):
    # Send a request to the URL with authentication credentials if provided
    response = requests.get(url, auth=auth)
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the breadcrumb microdata using the "itemtype" attribute
    breadcrumb = soup.find_all(itemtype=["https://schema.org/BreadcrumbList", "http://schema.org/BreadcrumbList"])
    if len(breadcrumb) > 0:
        return breadcrumb[0]
    else:
        return None

# Call the function to check for breadcrumb microdata
if url:
    if requires_auth == "Yes" and username and password:
        # Create a tuple of the username and password for authentication
        auth = (username, password)
        breadcrumb = check_breadcrumb_microdata(url, auth=auth)
        if breadcrumb:
            st.success("Breadcrumb microdata found!")
            # Check if the itemtype is deprecated
            deprecated = "http://schema.org/BreadcrumbList" in breadcrumb.get("itemtype")
            # Create a list of breadcrumb items
            breadcrumb_items = []
            # Display the breadcrumb microdata
            for item in breadcrumb.find_all(itemprop="itemListElement"):
                name = item.find(itemprop="name").text
                link = item.find(itemprop="item").get("href")
                position = item.find(itemprop="position").get("content")
                breadcrumb_items.append({"Name": name, "Link": link, "Position": position})
                #st.write(f"{name}: {link}: {position}")
                # Create a DataFrame to store the breadcrumb items
            breadcrumb_df = pd.DataFrame(breadcrumb_items)
            # Add a column to indicate if the itemtype is deprecated
            breadcrumb_df["Deprecated"] = deprecated
            # Display the DataFrame
            st.dataframe(breadcrumb_df)
        else:
            st.warning("No breadcrumb microdata found.")
    elif requires_auth == "Yes":
        st.warning("Please enter your username and password.")
    else:
        breadcrumb = check_breadcrumb_microdata(url)
        if breadcrumb:
            st.success("Breadcrumb microdata found!")
            # Check if the itemtype is deprecated
            deprecated = "http://schema.org/BreadcrumbList" in breadcrumb.get("itemtype")
            # Create a list of breadcrumb items
            breadcrumb_items = []
            for item in breadcrumb.find_all(itemprop="itemListElement"):
                name = item.find(itemprop="name").text
                link = item.find(itemprop="item").get("href")
                position = item.find(itemprop="position").get("content")
                breadcrumb_items.append({"Name": name, "Link": link, "Position": position})
                #st.write(f"{name}: {link}: {position}")
                # Create a DataFrame to store the breadcrumb items
            breadcrumb_df = pd.DataFrame(breadcrumb_items)
            # Add a column to indicate if the itemtype is deprecated
            breadcrumb_df["Deprecated"] = deprecated
            # Display the DataFrame
            st.dataframe(breadcrumb_df)
        else:
            st.warning("No breadcrumb microdata found.")
else:
    st.warning("Please enter a URL.")
