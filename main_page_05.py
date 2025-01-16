import streamlit as st
import base64

# 로컬 MP4 파일 경로 설정
video_path = "/mnt/c/data/shadowself_background.mp4"  # 비디오 파일 경로 수정

# MP4 비디오 파일을 Base64로 인코딩하는 함수
def video_to_base64(video_path):
    with open(video_path, "rb") as file_:
        video_contents = file_.read()
        video_base64 = base64.b64encode(video_contents).decode("utf-8")
    return video_base64

# Base64로 인코딩된 비디오 데이터 가져오기
video_base64 = video_to_base64(video_path)

# HTML 및 CSS 코드
video_html = f"""
    <style>
    #myVideo {{
      position: fixed;
      top: 50%;   /* 화면의 세로 중앙에 위치 */
      left: 50%;  /* 화면의 가로 중앙에 위치 */
      transform: translate(-50%, -50%);  /* 정확히 중앙에 맞추기 */
      min-width: 100%;
      min-height: 100%;
    }}
    </style>  
    <video autoplay muted loop id="myVideo">
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      Your browser does not support HTML5 video.
    </video>
"""

# HTML 마크업 렌더링
st.markdown(video_html, unsafe_allow_html=True)


