import streamlit as st
import json

st.title("👋 사람 목록 게시판")

# 사용자 데이터 로딩
with open("user_data.json", "r", encoding="utf-8") as file:
    users = json.load(file)

# 현재 사용자의 이름
current_user_name = st.session_state.get("name")

# List of pages
pages = {
    "🎡 choose the page": None,
    "🏠 home": "home.py",
    "🧑👧 friends": "./pages/friends_list.py",
    "🚧 logout": "pages/logout.py",

}

# Dropdown to select the page
selected_page = st.selectbox("Select a page:", list(pages.keys()))

    # 페이지 이동 처리
if pages[selected_page]:  # 선택된 페이지가 None이 아닐 경우
    st.switch_page(pages[selected_page])  # switch_page로 이동

# 사용자 목록 순회
for idx, user in enumerate(users):
    # 현재 사용자 제외
    if user["name"] == current_user_name:
        continue

    # 사용자 정보를 표시
    st.subheader(user["name"])  # 상대방 이름 표시
    col1, col2 = st.columns(2)

    with col1:
        # 대화하기 버튼: 이메일 값을 숨겨둠
        if st.button(f"💬 {user['name']}와 대화하기", key=f"chat_{user['email']}"):
            st.session_state["selected_person_email"] = user["email"]  # 선택한 친구의 이메일 저장
            st.session_state["selected_person_name"] = user["name"]  # 선택한 친구의 이름 저장
            st.switch_page("pages/chat.py")

    with col2:
        # 프로필 보기 버튼
        if st.button(f"📖 {user['name']} 프로필 보기", key=f"profile_{user['email']}"):
            st.info(f"**자기소개:** {user.get('bio', '자기소개가 없습니다.')}")

    # 연한 실선 추가 (HTML 사용)
   # if idx < len(users) - 1:  # 마지막 사용자 이후에는 선을 추가하지 않음
    st.markdown(
        """
        <hr style="border: 1px solid #ddd; margin: 10px 0;">
        """,
        unsafe_allow_html=True,
    )