import streamlit as st

# Updated rerun function using standard Streamlit session state updates
def rerun():
    st._set_query_params(dummy=str(st.session_state.get("rerun_count", 0)))
    if "rerun_count" not in st.session_state:
        st.session_state["rerun_count"] = 0
    st.session_state["rerun_count"] += 1

def main_page():
    st.write("Welcome to the main page!")

def profile_page(friend_name="User"):
    st.write(f"Profile of {friend_name}")
    st.write(f"Name: {friend_name}")
    st.write("Age: 25")
    st.write("Hobbies: Reading, Traveling")
    st.write("Interests: Chatting, Coding")
    if friend_name != "User" and st.button("Send Message"):
        chatroom_page(chat_partner=friend_name)

def chatrooms_page():
    st.write("Recent Chatrooms")
    recent_chatrooms = [
        {"name": "John", "last_message": "Hi! How are you?", "timestamp": "2024-12-27 10:00"},
        {"name": "Alice", "last_message": "Let’s meet tomorrow.", "timestamp": "2024-12-26 18:30"},
        {"name": "Bob", "last_message": "Can you call me?", "timestamp": "2024-12-25 14:15"}
    ]

    with st.container():
        for chat in recent_chatrooms:
            st.markdown(
                f"""
                <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 10px; cursor: pointer; max-width: 600px;' onclick="window.location.href='?dummy={chat['name']}';">
                    <div style='font-weight: bold; font-size: 18px;'>{chat['name']}</div>
                    <div style='margin-top: 5px;'>{chat['last_message']}</div>
                    <div style='text-align: right; color: grey; font-size: 12px;'>{chat['timestamp']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Enter {chat['name']}", key=f"chat_{chat['name']}"):
                st.session_state["current_page"] = "Chatroom"
                st.session_state["current_friend"] = chat['name']
                rerun()

def chatroom_page(chat_partner=None):
    if chat_partner:
        st.write(f"This is the chatroom with {chat_partner}.")
        with st.container():
            st.markdown(f"""
                <div style='border: 2px solid #ccc; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                    <p><b>Chat with {chat_partner}</b></p>
                    <textarea rows='10' style='width: 100%;'></textarea>
                    <button style='margin-top: 10px; background-color: #007bff; color: white; padding: 10px; border: none; border-radius: 5px;'>Send</button>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("This is a generic chatroom page.")

def friends_page():
    st.write("These are your favorite friends.")
    favorite_friends = [
        {"name": "John", "photo": "🧑"},
        {"name": "Alice", "photo": "👩"},
        {"name": "Bob", "photo": "👨"}
    ]
    for friend in favorite_friends:
        if st.button(f"{friend['photo']} {friend['name']}"):
            st.session_state["current_friend"] = friend['name']
            st.session_state["current_page"] = "Profile"
            rerun()

def recommended_friends_page():
    st.write("Here are some friend recommendations.")

# Sidebar menu for lists
with st.sidebar:
    st.title("Shadow Self")
    st.markdown("---")

    st.markdown("### Recent Messages")
    recent_contacts = [
        {"name": "John", "message": "Hi! How are you?", "unread": 2},
        {"name": "Alice", "message": "Let’s meet tomorrow.", "unread": 0},
        {"name": "Bob", "message": "Can you call me?", "unread": 1}
    ]
    st.write("<ul>", unsafe_allow_html=True)
    for contact in recent_contacts:
        st.markdown(f"<li><b>{contact['name']}</b>: {contact['message']} ({contact['unread']} new messages)</li>", unsafe_allow_html=True)
    st.write("</ul>", unsafe_allow_html=True)

    st.markdown("### Friends")
    favorite_friends = [
        {"name": "John", "photo": "🧑"},
        {"name": "Alice", "photo": "👩"},
        {"name": "Bob", "photo": "👨"}
    ]
    for friend in favorite_friends:
        st.markdown(f"{friend['photo']} {friend['name']}")

    st.markdown("### Search")
    search_query = st.text_input("Search")
    other_users = [
        {"name": "Tom", "photo": "👱"},
        {"name": "Jerry", "photo": "👦"},
        {"name": "Spike", "photo": "🐶"}
    ]
    if search_query:
        filtered_users = [user for user in other_users if search_query.lower() in user['name'].lower()]
    else:
        filtered_users = other_users
    for user in filtered_users:
        st.markdown(f"{user['photo']} {user['name']}")

# Navigation menu for page switching
def navigation_banner():
    pages = ["Main", "Profile", "Chatrooms", "Friends"]
    selected_page = None  # 초기값 설정
    cols = st.columns(len(pages))  # 페이지 수만큼 열 생성
    for col, page in zip(cols, pages):
        if col.button(page):  # 각 열에 버튼 배치
            if page == "Profile":
                st.session_state["current_friend"] = "User"  # Profile 클릭 시 User의 프로필
            st.session_state["current_page"] = page
    if selected_page is None:
        selected_page = st.session_state.get("current_page", "Main")  # 기본 페이지 설정
    return selected_page

# Display the navigation banner at the top of every page
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Main"

if "current_friend" not in st.session_state:
    st.session_state["current_friend"] = "User"

current_page = navigation_banner()

# Page content based on selection
menu_options = {
    "Main": main_page,
    "Profile": lambda: profile_page(friend_name=st.session_state["current_friend"]),
    "Chatrooms": chatrooms_page,
    "Chatroom": lambda: chatroom_page(chat_partner=st.session_state.get("current_friend")),
    "Friends": friends_page,
    "Recommended Friends": recommended_friends_page
}

st.session_state["current_page"] = current_page
menu_options[current_page]()
