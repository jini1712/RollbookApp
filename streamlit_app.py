import streamlit as st
import pandas as pd
from datetime import datetime

# 데이터 초기화
def initialize_data():
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=["날짜", "회원 이름", "체크"])

# 데이터 불러오기
def load_data(file_path):
    try:
        st.session_state.data = pd.read_csv(file_path)
        st.success("데이터를 성공적으로 불러왔습니다!")
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")

# 데이터 저장
def save_data(file_path):
    st.session_state.data.to_csv(file_path, index=False)
    st.success("데이터가 성공적으로 저장되었습니다!")

# 데이터 초기화
initialize_data()

# 제목
st.title("O/X 체크표 관리 시스템")

# 회원 관리
st.sidebar.header("회원 관리")
if "members" not in st.session_state:
    st.session_state.members = []

# 회원 추가/삭제
member_name = st.sidebar.text_input("회원 이름 추가", placeholder="예: 김철수")
if st.sidebar.button("회원 추가"):
    if member_name.strip() and member_name not in st.session_state.members:
        st.session_state.members.append(member_name)
        st.success(f"{member_name}이 추가되었습니다!")
    elif member_name in st.session_state.members:
        st.warning("이미 추가된 회원입니다.")
    else:
        st.warning("유효한 이름을 입력하세요.")

delete_member = st.sidebar.selectbox("회원 삭제", ["선택"] + st.session_state.members)
if st.sidebar.button("회원 삭제"):
    if delete_member != "선택":
        st.session_state.members.remove(delete_member)
        st.success(f"{delete_member}이 삭제되었습니다!")

st.sidebar.write("현재 회원 목록:")
st.sidebar.write(st.session_state.members)

# 데이터 로드
if st.sidebar.button("데이터 로드"):
    load_data("ox_checklist.csv")

# 날짜 선택
st.header("O/X 체크")
date = st.date_input("날짜 선택", value=datetime.now().date())

# 체크표
if not st.session_state.members:
    st.warning("회원 목록이 비어 있습니다. 회원을 추가해주세요.")
else:
    st.subheader(f"{date} 체크표")
    new_data = []
    for member in st.session_state.members:
        status = st.radio(f"{member}", ["O", "X", "미응답"], horizontal=True, key=f"{date}_{member}")
        new_data.append({"날짜": date, "회원 이름": member, "체크": status})

    if st.button("체크표 저장"):
        new_entries = pd.DataFrame(new_data)
        st.session_state.data = pd.concat([st.session_state.data, new_entries], ignore_index=True)
        st.success(f"{date} 체크표가 저장되었습니다!")

# 데이터 보기
st.header("전체 체크표 보기")
st.dataframe(st.session_state.data)

# 날짜별 필터링
st.header("날짜별 데이터 필터링")
filter_date = st.date_input("필터 날짜 선택", value=datetime.now().date(), key="filter_date")
filtered_data = st.session_state.data[st.session_state.data["날짜"] == str(filter_date)]
if not filtered_data.empty:
    st.write(f"{filter_date}의 체크 데이터:")
    st.dataframe(filtered_data)
else:
    st.write(f"{filter_date}에 해당하는 데이터가 없습니다.")

# 데이터 저장
if st.button("CSV로 저장"):
    save_data("ox_checklist.csv")

# 통계
st.header("O/X 통계")
if not st.session_state.data.empty:
    stats = st.session_state.data["체크"].value_counts()
    st.bar_chart(stats)
else:
    st.write("통계를 표시할 데이터가 없습니다.")
