import streamlit as st
import pandas as pd
from datetime import datetime

# 데이터 초기화 또는 로드
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["날짜", "회원 이름", "체크"])

data = load_data()

# 제목
st.title("O/X 체크표 관리 시스템")

# 회원 관리
st.sidebar.header("회원 관리")
members = st.sidebar.text_area("회원 목록 (각 줄에 한 명씩 입력)", placeholder="예: 김철수\n이영희")
member_list = members.split("\n")

# 날짜 선택
date = st.date_input("날짜 선택", value=datetime.now().date())

# 체크표
st.header(f"{date} O/X 체크표")
if not member_list or all(member.strip() == "" for member in member_list):
    st.warning("회원 목록을 입력해주세요.")
else:
    new_data = []
    for member in member_list:
        member = member.strip()
        if member:  # 빈 줄 무시
            status = st.radio(f"{member}", ["O", "X", "미응답"], horizontal=True)
            new_data.append({"날짜": date, "회원 이름": member, "체크": status})

    if st.button("체크표 저장"):
        new_entries = pd.DataFrame(new_data)
        global data
        data = pd.concat([data, new_entries], ignore_index=True)
        st.success(f"{date} 체크표가 저장되었습니다!")

# 체크표 보기
st.header("전체 체크표")
st.dataframe(data)

# 데이터 저장
if st.button("CSV로 저장"):
    data.to_csv("ox_checklist.csv", index=False)
    st.success("체크표가 CSV 파일로 저장되었습니다.")

# 통계
st.header("O/X 통계")
if not data.empty:
    stats = data["체크"].value_counts()
    st.bar_chart(stats)
else:
    st.write("체크 데이터가 없습니다.")
