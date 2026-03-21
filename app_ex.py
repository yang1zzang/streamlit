import streamlit as st
from datetime import date
import os

# 저장할 파일 이름
FILE_NAME = "book_records.txt"

# 페이지 상단 설정
st.title("독서 기록장")
st.text("읽은 책의 정보를 기록하고 TXT 파일로 저장합니다.")

# 입력 UI 부분
title = st.text_input("책 제목")
author = st.text_input("저자")
read_date = st.date_input("완독 날짜", value=date.today())
rating = st.select_slider("별점", options=[1, 2, 3, 4, 5])
memo = st.text_area("한 줄 감상 또는 메모")

# 저장 버튼 클릭 시 로직
if st.button("기록 추가하기"):
    if not title or not author:
        st.error("책 제목과 저자는 반드시 입력해야 합니다.")
    else:
        # 파일에 저장할 포맷 생성 (책제목/저자/날짜/별점/감상)
        # 줄바꿈 문자를 제거하여 한 줄에 한 기록이 들어가도록 처리
        clean_memo = memo.replace("\n", " ")
        record_line = f"{title}/{author}/{read_date}/{rating}/{clean_memo}\n"
        
        # 'a' (append) 모드로 파일 끝에 기록 추가
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(record_line)
        
        st.success("기록이 TXT 파일에 저장되었습니다.")

st.divider()

# 저장된 파일 내용 읽기 및 출력
st.subheader("최근 독서 기록")

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        # 모든 라인을 읽어와 리스트로 저장
        lines = f.readlines()
        
    # 최근 기록이 맨 위에 오도록 리스트 역순 정렬
    lines.reverse()

    for line in lines:
        # 슬래시(/)로 구분된 데이터 분리
        data = line.strip().split("/")
        
        # 데이터가 모든 항목을 포함하고 있는지 확인 후 출력
        if len(data) >= 5:
            with st.expander(f"{data[0]} - {data[1]}"):
                st.write(f"날짜: {data[2]}")
                st.write(f"별점: {data[3]} / 5")
                st.write(f"메모: {data[4]}")
else:
    st.info("저장된 기록 파일이 없습니다. 첫 기록을 작성해 보세요.")
