import streamlit as st
import hashlib
import json
import random

# Load user profiles from a JSON file (create one if it doesn't exist)
USER_PROFILES_FILE = "user_profiles.json"
try:
    with open(USER_PROFILES_FILE, "r") as file:
        user_profiles = json.load(file)
except FileNotFoundError:
    user_profiles = {}

# Load posts from a JSON file (create one if it doesn't exist)
POSTS_FILE = "posts.json"
try:
    with open(POSTS_FILE, "r") as file:
        posts = json.load(file)
except FileNotFoundError:
    posts = []

# Welcome screen
st.title("SocialSphere")
st.write("Welcome to SocialSphere - Your Simple Social Network!")

# Sidebar for navigation
menu = st.sidebar.radio("Menu", ["Welcome", "Register", "Create Post", "Random Posts", "User Profile"])

# Registration page
if menu == "Register":
    st.subheader("Registration Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_username in user_profiles:
            st.error("Username already exists!")
        elif new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Hash the password before storing
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            # Create an empty profile for the user
            user_profiles[new_username] = {"username": new_username, "bio": ""}
            # Store user profiles permanently
            with open(USER_PROFILES_FILE, "w") as file:
                json.dump(user_profiles, file)
            st.success("Registration successful! You can now create posts and view your profile.")

# Create post page
elif menu == "Create Post":
    st.subheader("Create Post")

    # Get current user's username
    if "username" in st.session_state:
        username = st.session_state["username"]
    else:
        username = "Anonymous"

    # Post form
    new_post = st.text_area("Write your post here", height=100)
    if st.button("Post"):
        if new_post.strip() != "":
            # Add the post to the list of posts
            posts.append({"author": username, "content": new_post})
            # Store posts permanently
            with open(POSTS_FILE, "w") as file:
                json.dump(posts, file)
            st.success("Post created successfully!")
        else:
            st.error("Post cannot be empty!")

# Random posts page
elif menu == "Random Posts":
    st.subheader("Random Posts")

    # Display all posts
    for post in posts:
        author = post["author"]
        content = post["content"]
        st.write(f"**Author:** {author}")
        st.write(content)

# User profile page
elif menu == "User Profile":
    st.subheader("User Profile")

    # Get current user's profile
    username = st.text_input("Enter Username")
    user_profile = user_profiles.get(username, {})
    st.write(f"**Username:** {user_profile.get('username', 'Anonymous')}")
    bio = st.text_area("Edit Bio", value=user_profile.get("bio", ""))
    if st.button("Save Bio"):
        user_profile["bio"] = bio
        user_profiles[username] = user_profile
        # Store profiles permanently
        with open(USER_PROFILES_FILE, "w") as file:
            json.dump(user_profiles, file)
        st.success("Bio updated successfully!")

# Display welcome screen
elif menu == "Welcome":
    st.subheader("Welcome!")
    st.write("This is SocialSphere - a simple social network where you can register, create posts, and view user profiles.")
    st.write("Use the tabs on the left to navigate.")
