import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib

# =========================
# 한글 폰트 설정 (깨짐 방지)
# =========================
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# =========================
# 감성 분석 모델 로드
# =========================
@st.cache_resource
def load_model():
    model_name = "matthewburke/korean_sentiment"
    return pipeline("sentiment-analysis", model=model_name)

model = load_model()

# =========================
# 파일 읽기
# =========================
def load_text(file):
    return file.read().decode("utf-8")

# =========================
# 문장 분리
# =========================
def split_sentences(text):
    return [s.strip() for s in text.split(".") if s.strip()]

# =========================
# 감성 분석
# =========================
def analyze_sentiment(sentences):
    return model(sentences)

# =========================
# 감성 단어 추출
# =========================
def extract_sentiment_words(sentences, results):
    words = {"POSITIVE": [], "NEGATIVE": []}

    for sent, res in zip(sentences, results):
        label = res["label"].upper()

        if "POS" in label:
            words["POSITIVE"].extend(sent.split())
        else:
            words["NEGATIVE"].extend(sent.split())

    return words

# =========================
# 원형 그래프 시각화
# =========================
def draw_pie_chart(results):
    labels = [r["label"] for r in results]
    counts = Counter(labels)

    fig, ax = plt.subplots()
    ax.pie(counts.values(), labels=counts.keys(), autopct="%1.1f%%")
    ax.set_title("감성 분석 결과")

    st.pyplot(fig)

# =========================
# Streamlit UI
# =========================
st.title("5.2.2 감성분석 시각화 프로그램")

# 1. 파일 업로드
uploaded_file = st.file_uploader("텍스트 파일 업로드 (.txt)", type=["txt"])

if uploaded_file:

    # 2. 파일 내용 보기
    text = load_text(uploaded_file)

    st.subheader("📄 파일 내용")
    st.write(text)

    # 문장 분리
    sentences = split_sentences(text)

    if st.button("감성 분석 실행"):

        # 3. 감성 분석
        results = analyze_sentiment(sentences)

        st.subheader("😊 감성 단어 영역")
        words = extract_sentiment_words(sentences, results)
        st.write(words)

        # 4. 감성 결과 출력
        st.subheader("📊 감성 분석 결과")
        st.write(results)

        # 5. 시각화
        st.subheader("📈 시각화 (원형 그래프)")
        draw_pie_chart(results)
