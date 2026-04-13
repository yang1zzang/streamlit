import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.font_manager as fm
import os

# =========================
# 1. 한글 폰트 설정
# =========================
def setup_font():
    # 교수님께서 확인하신 파일명으로 설정
    font_path = "NanumGothic-Regular.ttf" 
    
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
        plt.rcParams['axes.unicode_minus'] = False
        return True
    return False

has_font = setup_font()

# =========================
# 2. 모델 로드 (캐싱)
# =========================
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="matthewburke/korean_sentiment")

model = load_model()

# =========================
# 3. 분석 로직 (임계값 적용)
# =========================
def analyze_sentiment(sentences, threshold):
    raw_results = model(sentences)
    label_map = {"LABEL_1": "긍정", "LABEL_0": "부정"}
    
    processed_results = []
    for res in raw_results:
        # 모델의 확신 점수(score)가 슬라이더로 설정한 기준값보다 낮으면 '중립'으로 분류
        if res['score'] < threshold:
            label = "중립(확신부족)"
        else:
            label = label_map.get(res['label'], res['label'])
        
        processed_results.append({
            "label": label,
            "score": round(res['score'], 4)
        })
            
    return processed_results

# =========================
# 4. Streamlit UI (사이드바 추가)
# =========================
st.set_page_config(page_title="감성 분석 조절기", layout="wide")
st.title("🧪 감성 분석 문턱값(Threshold) 실습")

# 사이드바에서 학생들이 직접 기준치 조절
st.sidebar.header("⚙️ 분석 설정")
threshold_val = st.sidebar.slider(
    "긍정/부정 판단 기준선 (Threshold)", 
    min_value=0.5, 
    max_value=1.0, 
    value=0.8, 
    step=0.05,
    help="AI의 확신 점수가 이 값보다 높아야만 긍정 또는 부정으로 인정합니다."
)

uploaded_file = st.file_uploader("분석할 텍스트 파일(.txt)을 업로드하세요.", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    if st.button("분석 실행 및 시각화"):
        results = analyze_sentiment(sentences, threshold_val)
        
        # 레이아웃 분할
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"📊 감성 분포 (기준점: {threshold_val})")
            labels = [r["label"] for r in results]
            counts = Counter(labels)
            
            fig, ax = plt.subplots()
            ax.pie(counts.values(), labels=counts.keys(), autopct="%1.1f%%", startangle=90)
            st.pyplot(fig)

        with col2:
            st.subheader("📝 상세 분석 결과")
            # 데이터프레임 형태로 출력하여 점수(Score) 확인 용이하게 함
            st.dataframe(results, use_container_width=True)

        # 데이터 리터러시 가이드라인
        st.divider()
        st.markdown(f"""
        ### 💡 데이터 리터러시 포인트
        - 현재 설정된 **문턱값({threshold_val})**보다 낮은 확신을 가진 문장들은 **'중립(확신부족)'**으로 분류되었습니다.
        - 슬라이더를 높일수록 AI가 아주 확실할 때만 긍정/부정으로 분류하므로 결과가 더 엄격해집니다.
        - 반대로 낮추면 AI가 조금만 의심되어도 긍정/부정으로 분류하여 그래프의 비율이 크게 변합니다.
        """)

elif not has_font:
    st.error("NanumGothic-Regular.ttf 파일을 찾을 수 없습니다. 파일을 업로드해 주세요.")
