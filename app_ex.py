import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.font_manager as fm
import os

# =========================
# 1. 한글 폰트 설정 (배포 환경 대응)
# =========================
def setup_font():
    # GitHub에 함께 올린 폰트 파일 이름
    font_path = "NanumGothic-Regular.ttf" 
    
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        font_name = font_prop.get_name()
        plt.rc('font', family=font_name)
        plt.rcParams['axes.unicode_minus'] = False

has_font = setup_font()

# =========================
# 2. 감성 분석 모델 로드
# =========================
@st.cache_resource
def load_model():
    # 한국어 감성 분석에 특화된 모델
    model_name = "matthewburke/korean_sentiment"
    return pipeline("sentiment-analysis", model=model_name)

model = load_model()

# =========================
# 3. 주요 기능 함수들
# =========================
def load_text(file):
    return file.read().decode("utf-8")

def split_sentences(text):
    return [s.strip() for s in text.split(".") if s.strip()]

def analyze_sentiment(sentences):
    raw_results = model(sentences)
    # 레이블 변환 맵 (LABEL_1: 긍정, LABEL_0: 부정)
    label_map = {"LABEL_1": "긍정", "LABEL_0": "부정"}
    
    for res in raw_results:
        res['label'] = label_map.get(res['label'], res['label'])
    return raw_results

def extract_sentiment_words(sentences, results):
    words = {"긍정": [], "부정": []}
    for sent, res in zip(sentences, results):
        label = res["label"]
        if label == "긍정":
            words["긍정"].extend(sent.split())
        else:
            words["부정"].extend(sent.split())
    return words

def draw_pie_chart(results):
    labels = [r["label"] for r in results]
    counts = Counter(labels)

    fig, ax = plt.subplots()
    # 한글 레이블이 적용된 데이터로 차트 생성
    ax.pie(counts.values(), labels=counts.keys(), autopct="%1.1f%%", startangle=90)
    ax.set_title("전체 감성 분포")
    st.pyplot(fig)

# =========================
# 4. Streamlit UI
# =========================
st.set_page_config(page_title="감성 분석기", layout="wide")
st.title("📊 데이터 리터러시: 감성 분석 시각화")

if not has_font:
    st.info("💡 배포 환경에서는 NanumGothic.ttf 파일을 업로드해야 한글이 깨지지 않습니다.")

uploaded_file = st.file_uploader("분석할 텍스트 파일(.txt)을 업로드하세요.", type=["txt"])

if uploaded_file:
    text = load_text(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 원문 내용")
        st.info(text[:500] + ("..." if len(text) > 500 else ""))

    if st.button("감성 분석 실행"):
        sentences = split_sentences(text)
        results = analyze_sentiment(sentences)
        words = extract_sentiment_words(sentences, results)

        with col2:
            st.subheader("📈 시각화 결과")
            draw_pie_chart(results)

        st.divider()
        
        # 상세 결과 섹션
        tab1, tab2 = st.tabs(["😊 감성 단어 분류", "📝 문장별 분석 결과"])
        
        with tab1:
            st.write(words)
            
        with tab2:
            st.table(results)
