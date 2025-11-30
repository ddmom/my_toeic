import streamlit as st
import pandas as pd
import random

# ---------------------------------------------------------
# [수정된 부분] 1. 앱 설정 (최적화된 아이콘 적용)
# ---------------------------------------------------------
# 'lighthouse-icon-small.png' 파일이 깃허브(같은 폴더)에 있어야 합니다.
st.set_page_config(
    page_title="토익 마스터",
    page_icon="lighthouse-icon-small.png",  # <--- 변환된 파일명으로 연결했습니다!
    layout="centered"
)

# CSS 스타일
st.markdown("""
    <style>
    .big-font { font-size: 30px !important; font-weight: bold; color: #333; }
    .vs-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;}
    .explanation { background-color: #fff3cd; padding: 15px; border-radius: 5px; color: #856404; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바(메뉴)
menu = st.sidebar.selectbox("메뉴 선택", ["1. 단어 암기장", "2. 헷갈리는 단어 VS 게임"])

# ---------------------------------------------------------
# [기능 1] 단어 암기장
# ---------------------------------------------------------
if menu == "1. 단어 암기장":
    st.title("📘 토익 단어 암기장")
    
    try:
        df = pd.read_excel("toeic_words.xlsx")
        # 컬럼 이름 강제 통일 (오류 방지)
        if len(df.columns) >= 4:
            df.columns = ['English', 'Korean', 'Synonyms', 'Example']
        elif len(df.columns) == 3:
            df.columns = ['English', 'Korean', 'Synonyms']
            
        if 'current_word' not in st.session_state:
            st.session_state.current_word = df.sample(1).iloc[0]
            st.session_state.show_answer_1 = False

        word = st.session_state.current_word

        st.markdown(f"<div style='text-align: center; font-size: 40px; color: #4A90E2;'><b>{word['English']}</b></div>", unsafe_allow_html=True)
        st.write("")

        if st.button("정답 보기", key="btn1"):
            st.session_state.show_answer_1 = True
            st.rerun()

        if st.session_state.show_answer_1:
            st.success(f"뜻: {word['Korean']}")
            if 'Example' in word: # 예문 컬럼이 있을 때만 표시
                st.info(f"예문: {word['Example']}")
            
            if st.button("다음 단어 ->", key="next1"):
                st.session_state.current_word = df.sample(1).iloc[0]
                st.session_state.show_answer_1 = False
                st.rerun()

    except Exception as e:
        st.error(f"오류: 'toeic_words.xlsx' 파일을 읽을 수 없습니다. ({e})")

# ---------------------------------------------------------
# [기능 2] 헷갈리는 단어 VS 게임
# ---------------------------------------------------------
elif menu == "2. 헷갈리는 단어 VS 게임":
    st.title("⚔️ 헷갈리는 단어 VS")
    st.markdown("문맥에 맞는 올바른 단어를 고르세요!")

    try:
        # 데이터 로드
        df_vs = pd.read_excel("vs_quiz.xlsx")
        
        # 엑셀 제목 강제 통일
        if len(df_vs.columns) >= 4:
            df_vs.columns = ['Question', 'Correct', 'Wrong', 'Explanation']
        else:
            st.error("엑셀 파일에 열(세로칸)이 4개 부족합니다. (문제, 정답, 오답, 해설)")

        # 문제 초기화
        if 'vs_q' not in st.session_state:
            row = df_vs.sample(1).iloc[0]
            st.session_state.vs_q = row
            options = [row['Correct'], row['Wrong']]
            random.shuffle(options)
            st.session_state.options = options
            st.session_state.solved = False
            st.session_state.result_msg = ""

        q = st.session_state.vs_q

        # 화면 표시
        st.markdown(f"<div class='vs-box'><span class='big-font'>{q['Question']}</span></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        # 버튼 1
        with col1:
            if st.button(st.session_state.options[0], use_container_width=True, disabled=st.session_state.solved):
                if st.session_state.options[0] == q['Correct']:
                    st.session_state.result_msg = "correct"
                else:
                    st.session_state.result_msg = "wrong"
                st.session_state.solved = True
                st.rerun()

        # 버튼 2
        with col2:
            if st.button(st.session_state.options[1], use_container_width=True, disabled=st.session_state.solved):
                if st.session_state.options[1] == q['Correct']:
                    st.session_state.result_msg = "correct"
                else:
                    st.session_state.result_msg = "wrong"
                st.session_state.solved = True
                st.rerun()

        # 결과 및 해설
        if st.session_state.solved:
            if st.session_state.result_msg == "correct":
                st.balloons()
                st.success(f"✅ 정답입니다! ({q['Correct']})")
            else:
                st.error(f"❌ 땡! 정답은 '{q['Correct']}' 입니다.")
            
            # 해설 박스
            if pd.notna(q['Explanation']):
                st.markdown(f"<div class='explanation'>💡 <b>해설:</b> {q['Explanation']}</div>", unsafe_allow_html=True)
            st.write("")

            # 다음 문제
            if st.button("다음 문제 도전 ➡", type="primary"):
                row = df_vs.sample(1).iloc[0]
                st.session_state.vs_q = row
                options = [row['Correct'], row['Wrong']]
                random.shuffle(options)
                st.session_state.options = options
                st.session_state.solved = False
                st.session_state.result_msg = ""
                st.rerun()

    except Exception as e:
        st.error(f"오류: 엑셀 파일을 읽는 중 문제가 생겼습니다. ({e})")