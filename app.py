import streamlit as st
import pandas as pd
import random

# 1. 앱 설정 & 게임 스타일 CSS
st.set_page_config(page_title="토익 700 영단어 게임", layout="centered")

st.markdown("""
    <style>
    /* 점수판 스타일 */
    .metric-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    /* 단어 폰트 */
    .big-font { font-size: 50px !important; color: #4A90E2; font-weight: bold; }
    .meaning { font-size: 32px !important; font-weight: bold; color: #333; }
    
    /* 박스 스타일 */
    .synonym-box { background-color: #fff3cd; padding: 15px; border-radius: 10px; margin-bottom: 10px; color: #856404; font-size: 20px !important; }
    .example-box { background-color: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 8px solid #4A90E2; font-style: italic; font-size: 22px !important; color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("toeic_words.xlsx")
        # 컬럼명 강제 통일
        expected_cols = ['English', 'Korean', 'Synonyms', 'Example']
        if len(df.columns) >= 4:
            df.columns = expected_cols[:len(df.columns)] + df.columns.tolist()[len(expected_cols):] # 이름 매핑
            df.columns.values[0] = 'English'
            df.columns.values[1] = 'Korean'
            df.columns.values[2] = 'Synonyms'
            df.columns.values[3] = 'Example'
        elif len(df.columns) == 3:
            df.columns.values[0] = 'English'
            df.columns.values[1] = 'Korean'
            df.columns.values[2] = 'Synonyms'
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 3. 게임 상태(변수) 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'total_count' not in st.session_state:
    st.session_state.total_count = 0
if 'current_word' not in st.session_state:
    if not df.empty:
        st.session_state.current_word = df.sample(1).iloc[0]
    else:
        st.session_state.current_word = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# 함수: 정답 처리 (점수 획득)
def correct_answer():
    st.session_state.score += 10 + (st.session_state.combo * 2) # 콤보 보너스!
    st.session_state.combo += 1
    st.session_state.total_count += 1
    st.balloons() # 축하 효과
    next_word()

# 함수: 오답 처리 (점수 유지, 콤보 초기화)
def wrong_answer():
    st.session_state.combo = 0 # 콤보 끊김 ㅠㅠ
    st.session_state.total_count += 1
    next_word()

def next_word():
    st.session_state.current_word = df.sample(1).iloc[0]
    st.session_state.show_answer = False

# 함수: 게임 리셋
def reset_game():
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.total_count = 0
    next_word()

# 4. 화면 구성
st.title("🎮 토익 700점 랭킹전")

# 점수판 (Metrics)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric(label="🏆 내 점수 (XP)", value=f"{st.session_state.score}")
with col_b:
    st.metric(label="🔥 연속 정답 (Combo)", value=f"{st.session_state.combo}")
with col_c:
    st.metric(label="📚 학습한 단어", value=f"{st.session_state.total_count}개")

st.markdown("---")

if df.empty:
    st.error("엑셀 파일이 없습니다! toeic_words.xlsx를 확인하세요.")
else:
    word = st.session_state.current_word
    
    # 1) 문제 (영어 단어)
    st.markdown(f"<div style='text-align: center;'><span class='big-font'>{word['English']}</span></div>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # 2) 정답 확인 버튼
    if not st.session_state.show_answer:
        if st.button("🔍 정답 확인 (Click)", use_container_width=True, type="primary"):
            st.session_state.show_answer = True
            st.rerun()
    
    # 3) 정답 공개 및 채점
    else:
        # 뜻 보여주기
        st.markdown(f"<div style='text-align: center;' class='meaning'>{word['Korean']}</div>", unsafe_allow_html=True)
        st.write("")

        # 유사어 & 예문
        if 'Synonyms' in word and pd.notna(word['Synonyms']):
            st.markdown(f"<div class='synonym-box'>🔄 <b>유사어:</b> {word['Synonyms']}</div>", unsafe_allow_html=True)
        if 'Example' in word and pd.notna(word['Example']):
            st.markdown(f"<div class='example-box'>📝 <b>예문:</b><br>{word['Example']}</div>", unsafe_allow_html=True)
        
        st.write("")
        
        # 게임 버튼 (O / X)
        col1, col2 = st.columns(2)
        with col1:
            # 알아요 버튼
            if st.button("✅ 알아요 (+10점)", use_container_width=True):
                correct_answer()
                st.rerun()
        with col2:
            # 몰라요 버튼
            if st.button("❌ 몰라요 (복습)", use_container_width=True):
                wrong_answer()
                st.rerun()

# 5. 하단 리셋 버튼
st.markdown("---")
if st.button("🔄 점수 초기화 (처음부터 다시)"):
    reset_game()
    st.rerun()