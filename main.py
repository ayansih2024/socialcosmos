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

# Save group data to file
def save_groups():
    with open(GROUPS_FILE, "w") as file:
        json.dump(groups, file)

st.markdown(
    """
    <style>
    /* Global Page Background Gradient */
    .main {
        background: linear-gradient(to right, #333, #000); /* Same gradient as buttons */
        color: white;
        text-align: center;
        padding: 40px;
        border-radius: 10px;
        position: relative;
    }

    /* Buttons Styling */
    .button, .stButton > button {
        padding: 1em 2em;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        letter-spacing: 5px;
        text-transform: uppercase;
        cursor: pointer;
        color: #2c9caf;
        transition: all 1000ms;
        font-size: 15px;
        position: relative;
        overflow: hidden;
        outline: 2px solid #2c9caf;
        background: linear-gradient(to right, #333, #000); /* Same gradient */
    }
    .button:hover, .stButton > button:hover {
        color: #ffffff;
        transform: scale(1.1);
        outline: 2px solid #70bdca;
        box-shadow: 4px 5px 17px -4px #268391;
    }
    .button::before, .stButton > button::before {
        content: "";
        position: absolute;
        left: -50px;
        top: 0;
        width: 0;
        height: 100%;
        background-color: #2c9caf;
        transform: skewX(45deg);
        z-index: -1;
        transition: width 1000ms;
    }
    .button:hover::before, .stButton > button:hover::before {
        width: 250%;
    }

    /* Text Input, Textarea, and Select Styling */
    input, textarea, select, .stTextInput > div > input, .stTextArea > div > textarea, .stSelectbox > div > select {
        background: #222;
        color: white;
        border: 1px solid #555;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    input:focus, textarea:focus, select:focus, .stTextInput > div > input:focus, .stTextArea > div > textarea:focus, .stSelectbox > div > select:focus {
        border-color: #777;
        outline: none;
    }

    /* Titles and Headers */
    .title {
        font-size: 40px;
        font-weight: bold;
        font-style: italic;
    }
    .subtitle {
        font-size: 20px;
        font-weight: lighter;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Function to render header with theme
# Adjusted to appear only on Welcome page
def render_header():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="circle">Use the tabs on the left to navigate.<br><span class="arrow">⬅</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="title">SocialSphere</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Welcome to SocialSphere - Your Simple Social Network!</p>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<p class="box">PLEASE LOG IN TO MANAGE FRIENDS.</p>', unsafe_allow_html=True)
    st.markdown('<br><br>', unsafe_allow_html=True)

# Function to authenticate user
def authenticate_user(username, password):
    if username in user_profiles:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == user_profiles[username]["password"]
    return False

# Functions for group management
def create_group(group_name, creator):
    if group_name not in groups:
        groups[group_name] = {"creator": creator, "members": [creator]}
        save_groups()
        return True
    return False

def join_group(group_name, username):
    if group_name in groups and username not in groups[group_name]["members"]:
        groups[group_name]["members"].append(username)
        save_groups()
        return True
    return False

def leave_group(group_name, username):
    if group_name in groups and username in groups[group_name]["members"]:
        groups[group_name]["members"].remove(username)
        save_groups()
        return True
    return False

def add_group_message(group_name, sender, content):
    if group_name not in messages:
        messages[group_name] = []
    messages[group_name].append({"sender": sender, "content": content})
    with open(MESSAGES_FILE, "w") as file:
        json.dump(messages, file)

# Menu-based navigation
# Menu-based navigation
menu = st.sidebar.radio("Menu", [
    "Welcome", "Register", "Login", "Create Post", "Random Posts", 
    "User Profile", "Chat", "Video Call", "Group Management", 
    "Group Chat", "Documentation", "About"
])

if menu == "Welcome":
    render_header()
    st.write("This is SocialCosmos - a simple social network where you can register, log in, create posts, view user profiles, chat with other users, and browse random posts.")

elif menu == "Documentation":
    st.title("Documentation")
    st.write("Welcome to the SocialSphere Documentation! Here's how to use the app:")
    
    st.subheader("1. Register")
    st.write("""
    - Go to the **Register** page in the sidebar.
    - Enter a unique username and password.
    - Confirm your password and click on the **Register** button.
    - After successful registration, log in using your credentials.
    """)

    st.subheader("2. Login")
    st.write("""
    - Navigate to the **Login** page.
    - Enter your registered username and password.
    - Click on the **Login** button to access your account.
    """)

    st.subheader("3. Create Post")
    st.write("""
    - Go to the **Create Post**b page.
    - Write your post in the text area.
    - Optionally, upload an image to attach to your post.
    - Click on **Post** to share your content.
    """)

    st.subheader("4. View Random Posts")
    st.write("""
    - Visit the **Random Posts** page to explore content shared by others.
    - If a post contains an image, it will be displayed below the text.
    """)

    st.subheader("5. User Profile")
    st.write("""
    - Use the **User Profile** page to view and update your bio.
    - Enter a username to view their profile or update your own.
    """)

    st.subheader("6. Chat and Group Features")
    st.write("""
    - **Chat**: Select a user to chat with, type your message, and send it.
    - **Group Management**: Create, join, or leave groups using this page.
    - **Group Chat**: Communicate with group members by sending group messages.
    """)

    st.subheader("7. Video Call")
    st.write("""
    - Use the **Video Call** page to start a real-time video call with other users.
    """)

    st.subheader("8. Security and Privacy")
    st.write("""
    - Your passwords are securely hashed using SHA256.
    - Messages and posts are stored locally in JSON files (can be upgraded to a database for better scalability).
    """)
    
    st.info("For further assistance or questions, contact the SocialSphere development team! Message on +91 8767273849")

# Keep the rest of the menu logic as is...


elif menu == "Register":
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
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user_profiles[new_username] = {"username": new_username, "password": hashed_password, "bio": ""}
            with open(USER_PROFILES_FILE, "w") as file:
                json.dump(user_profiles, file)
            st.success("Registration successful! You can now log in.")

elif menu == "Login":
    st.subheader("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password!")

elif menu == "Create Post":
    st.subheader("Create Post")
    new_post = st.text_area("Write your post here", height=100)
    uploaded_file = st.file_uploader("Upload image for the post (optional)", type=["jpg", "jpeg", "png"])

    if st.button("Post"):
        if new_post.strip() != "":
            post_data = {"content": new_post}
            if uploaded_file is not None:
                image_data = uploaded_file.read()
                post_data["image"] = base64.b64encode(image_data).decode('utf-8')
            posts.append(post_data)
            with open(POSTS_FILE, "w") as file:
                json.dump(posts, file)
            st.success("Post created successfully!")
        else:
            st.error("Post cannot be empty!")

elif menu == "Random Posts":
    st.subheader("Random Posts")
    for post in posts:
        content = post["content"]
        st.write(content)
        if "image" in post:
            image_data = base64.b64decode(post["image"])
            st.image(image_data, caption='Uploaded Image', use_column_width=True)

elif menu == "User Profile":
    st.subheader("User Profile")
    username = st.text_input("Enter Username")
    if username in user_profiles:
        st.write(f"**Username:** {username}")
        st.write(f"**Bio:** {user_profiles[username].get('bio', 'No bio available.')}")
        bio = st.text_area("Update Bio", value=user_profiles[username].get("bio", ""))
        if st.button("Save Bio"):
            user_profiles[username]["bio"] = bio
            with open(USER_PROFILES_FILE, "w") as file:
                json.dump(user_profiles, file)
            st.success("Bio updated successfully!")
    else:
        st.error("User not found!")

elif menu == "Chat":
    st.subheader("Chat")
    selected_user = st.selectbox("Select User", list(user_profiles.keys()))
    st.write("Chat with other users here!")
    new_message = st.text_input("Type your message")
    if st.button("Send Message"):
        if new_message.strip() != "":
            if selected_user not in messages:
                messages[selected_user] = []
            messages[selected_user].append({"sender": "You", "content": new_message})
            with open(MESSAGES_FILE, "w") as file:
                json.dump(messages, file)
            st.success("Message sent successfully!")

elif menu == "Group Chat":
    st.subheader("Group Chat")
    group_name = st.selectbox("Select Group", [group for group, data in groups.items() if "You" in data["members"]])
    if group_name:
        st.write(f"Group: {group_name}")
        st.write("Messages:")
        if group_name in messages:
            for msg in messages[group_name]:
                st.write(f"{msg['sender']}: {msg['content']}")
        new_group_message = st.text_input("Type your message for the group")
        if st.button("Send Group Message"):
            if new_group_message.strip():
                add_group_message(group_name, "You", new_group_message)
                st.success("Message sent to group!")

elif menu == "Video Call":
    st.subheader("Video Call")
    st.write("Start a video call with other users!")
    webrtc_streamer(key="example")

elif menu == "Group Management":
    st.subheader("Group Management")

    st.subheader("Create a Group")
    group_name = st.text_input("Enter group name")
    if st.button("Create Group"):
        if create_group(group_name, "You"):
            st.success(f"Group '{group_name}' created successfully!")
        else:
            st.error("Group already exists!")

    st.subheader("Join a Group")
    join_group_name = st.text_input("Enter group name to join")
    if st.button("Join Group"):
        if join_group(join_group_name, "You"):
            st.success(f"Joined group '{join_group_name}' successfully!")
        else:
            st.error("Group does not exist or you are already a member!")

elif menu == "About":
    st.subheader("About")
    st.write("This application was created by The SocialCosmos team.")
    st.write("**Programmers:**")
    st.write("- Ayan Gantayat")
    st.write("**Designers:**")
    st.write("- Shreemoyee Shaw")
    st.write("- Sanah Pathak")
