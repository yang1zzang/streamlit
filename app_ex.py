import streamlit as st
from datetime import date

# 페이지 상단 제목 및 설명
st.title("독서 기록장")
st.text("읽은 책의 정보를 기록하고 관리하는 공간입니다.")

# 세션 상태에 기록 저장용 리스트 초기화
if "book_logs" not in st.session_state:
    st.session_state.book_logs = []

# 입력 UI 부분
with st.container():
    title = st.text_input("책 제목")
    author = st.text_input("저자")
    read_date = st.date_input("완독 날짜", value=date.today())
    rating = st.select_slider("별점", options=[1, 2, 3, 4, 5])
    memo = st.text_area("한 줄 감상 또는 메모")

    # 저장 버튼
    if st.button("저장하기"):
        # 유효성 검사: 제목과 저자 필수 입력
        if not title or not author:
            st.error("책 제목과 저자는 반드시 입력해야 합니다.")
        else:
            # 기록 저장 (딕셔너리 형태)
            new_log = {
                "title": title,
                "author": author,
                "date": read_date,
                "rating": rating,
                "memo": memo
            }
            # 리스트의 맨 앞에 추가하여 최근 기록이 위로 오게 함
            st.session_state.book_logs.insert(0, new_log)
            st.success("기록이 성공적으로 저장되었습니다.")

st.divider()

# 저장된 기록 목록 표시
st.subheader("최근 독서 기록")

if not st.session_state.book_logs:
    st.info("저장된 기록이 없습니다.")
else:
    for log in st.session_state.book_logs:
        # 각 기록을 구분하기 위한 컨테이너
        with st.expander(f"{log['title']} - {log['author']}"):
            st.write(f"날짜: {log['date']}")
            st.write(f"별점: {log['rating']} / 5")
            st.write(f"메모: {log['memo']}")
