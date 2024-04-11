import streamlit as st
import hashlib
import json
import base64
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

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

# Load messages from a JSON file (create one if it doesn't exist)
MESSAGES_FILE = "messages.json"
try:
    with open(MESSAGES_FILE, "r") as file:
        messages = json.load(file)
except FileNotFoundError:
    messages = {}

# Load groups from a JSON file (create one if it doesn't exist)
GROUPS_FILE = "groups.json"
try:
    with open(GROUPS_FILE, "r") as file:
        groups = json.load(file)
except FileNotFoundError:
    groups = {}

# Function to authenticate user
def authenticate_user(username, password):
    if username in user_profiles:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == user_profiles[username]["password"]
    return False

# Function to create a new group
def create_group(group_name, creator):
    if group_name not in groups:
        groups[group_name] = {"creator": creator, "members": [creator]}
        return True
    return False

# Function to join a group
def join_group(group_name, username):
    if group_name in groups:
        groups[group_name]["members"].append(username)
        return True
    return False

# Function to leave a group
def leave_group(group_name, username):
    if group_name in groups and username in groups[group_name]["members"]:
        groups[group_name]["members"].remove(username)
        return True
    return False

# Welcome screen
st.title("SocialCosmos")
st.write("Welcome to SocialCosmos - Your Simple Social Network!")

# Sidebar for navigation
menu = st.sidebar.radio("Menu", ["Welcome", "Register", "Login", "Create Post", "Random Posts", "User Profile", "Chat", "Video Call", "Group Management", "Group Chat", "About"])

# Check if user is already logged in
if "username" in st.session_state:
    current_user = st.session_state["username"]
else:
    current_user = None

# Remember me checkbox
remember_me = st.sidebar.checkbox("Remember Me")

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
            user_profiles[new_username] = {"username": new_username, "password": hashed_password, "bio": ""}
            # Store user profiles permanently
            with open(USER_PROFILES_FILE, "w") as file:
                json.dump(user_profiles, file)
            st.success("Registration successful! You can now log in.")

# Login page
if menu == "Login":
    st.subheader("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            current_user = username
            if remember_me:
                st.session_state["username"] = username
        else:
            st.error("Invalid username or password!")

# Create post page
if menu == "Create Post":
    st.subheader("Create Post")

    # Post form
    new_post = st.text_area("Write your post here", height=100)
    uploaded_file = st.file_uploader("Upload image for the post (optional)", type=["jpg", "jpeg", "png"])

    if st.button("Post"):
        if new_post.strip() != "":
            # Add the post to the list of posts
            post_data = {"author": current_user, "content": new_post}
            if uploaded_file is not None:
                image_data = uploaded_file.read()
                post_data["image"] = base64.b64encode(image_data).decode('utf-8')
            posts.append(post_data)
            # Store posts permanently
            with open(POSTS_FILE, "w") as file:
                json.dump(posts, file)
            st.success("Post created successfully!")
        else:
            st.error("Post cannot be empty!")

# Random posts page
if menu == "Random Posts":
    st.subheader("Random Posts")

    # Display all posts
    for post in posts:
        author = post["author"]
        content = post["content"]
        st.write(f"**Author:** {author}")
        st.write(content)
        if "image" in post:
            image_data = base64.b64decode(post["image"])
            st.image(image_data, caption='Uploaded Image', use_column_width=True)

# User profile page
if menu == "User Profile":
    st.subheader("User Profile")

    user_profile = user_profiles.get(current_user, {})
    st.write(f"**Username:** {user_profile.get('username', 'Anonymous')}")
    bio = st.text_area("Edit Bio", value=user_profile.get("bio", ""))
    if st.button("Save Bio"):
        user_profile["bio"] = bio
        user_profiles[current_user] = user_profile
        # Store profiles permanently
        with open(USER_PROFILES_FILE, "w") as file:
            json.dump(user_profiles, file)
        st.success("Bio updated successfully!")

# Chat page
if menu == "Chat":
    st.subheader("Chat")

    # Select user to chat with
    selected_user = st.selectbox("Select User", list(user_profiles.keys()))

    # Display chat history
    if selected_user in messages:
        st.write("Chat History:")
        for message in messages[selected_user]:
            st.write(f"{message['sender']}: {message['content']}")
    else:
        st.write("No chat history available.")

    # Input message
    new_message = st.text_input("Type your message:")
    if st.button("Send"):
        if new_message.strip() != "":
            if selected_user not in messages:
                messages[selected_user] = []
            messages[selected_user].append({"sender": current_user, "content": new_message})
            # Store messages permanently
            with open(MESSAGES_FILE, "w") as file:
                json.dump(messages, file)
            st.success("Message sent successfully!")
        else:
            st.error("Message cannot be empty!")

# Video call page
if menu == "Video Call":
    st.subheader("Video Call")

    st.write("Select user to call:")
    user_to_call = st.selectbox("Select User", list(user_profiles.keys()))

    # Video call streamer
    webrtc_streamer(key=f"video-call-{user_to_call}",
                    video_processor_factory=VideoTransformerBase,
                    async_transform=True,
                    )

# Group management page
if menu == "Group Management":
    st.subheader("Group Management")

    # Create a new group form
    st.subheader("Create a New Group")
    new_group_name = st.text_input("Enter the group name:")
    if st.button("Create Group"):
        if create_group(new_group_name, current_user):
            st.success(f"Group '{new_group_name}' created successfully!")
        else:
            st.error("Group name already exists!")

    # Join a group form
    st.subheader("Join an Existing Group")
    join_group_name = st.text_input("Enter the group name to join:")
    if st.button("Join Group"):
        if join_group(join_group_name, current_user):
            st.success(f"Joined group '{join_group_name}' successfully!")
        else:
            st.error("Group does not exist!")

    # Leave a group form
    st.subheader("Leave a Group")
    leave_group_name = st.text_input("Enter the group name to leave:")
    if st.button("Leave Group"):
        if leave_group(leave_group_name, current_user):
            st.success(f"Left group '{leave_group_name}' successfully!")
        else:
            st.error("You are not a member of this group!")

# Group chat page
if menu == "Group Chat":
    st.subheader("Group Chat")

    # Select group to chat in
    selected_group = st.selectbox("Select Group", list(groups.keys()))

    # Display group members
    if selected_group in groups:
        st.write("Group Members:")
        for member in groups[selected_group]["members"]:
            st.write(member)
    else:
        st.write("No group selected.")

    # Display group chat history
    if selected_group in messages:
        st.write("Group Chat History:")
        for message in messages[selected_group]:
            st.write(f"{message['sender']}: {message['content']}")
    else:
        st.write("No chat history available.")

    # Input message
    new_group_message = st.text_input("Type your message:")
    if st.button("Send"):
        if new_group_message.strip() != "":
            if selected_group not in messages:
                messages[selected_group] = []
            messages[selected_group].append({"sender": current_user, "content": new_group_message})
            # Store messages permanently
            with open(MESSAGES_FILE, "w") as file:
                json.dump(messages, file)
            st.success("Message sent successfully!")
        else:
            st.error("Message cannot be empty!")

# About page
if menu == "About":
    st.subheader("About")
    st.write("This application was created by The SocialCosmos team.")
    st.write("Programmers:")
    st.write("- Ayan Gantayat")
    st.write("- Radek Katyal")
    st.write("Designer:")
    st.write("- Animi Yakshit")         
   

# Display welcome screen
if menu == "Welcome":
    st.subheader("Welcome!")
    st.write("This is SocialCosmos - a place where you can hang out and make yourself cozy")
    st.write("Use the tabs on the left to navigate.")
