import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- 페이지 설정 및 제목 ---
st.set_page_config(page_title="AI 엑셀 필터 분류기", page_icon="📊")
st.title("📊 AI 엑셀 필터 분류 프로그램")
st.write("분류하고 싶은 엑셀 파일을 업로드하면, AI가 파일의 필터(첫 행)를 분석하여 분류해줍니다.")

# --- API 키 설정 ---
# Streamlit 배포 환경에서는 st.secrets를 통해 API 키를 안전하게 가져옵니다.
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("오류: Streamlit Secrets에 API 키가 설정되지 않았습니다. 배포 설정에서 API 키를 등록해주세요.")
    st.stop()

# --- AI 모델 설정 (비용이 가장 저렴한 Flash 모델 사용) ---
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction="당신은 엑셀 파일의 헤더(필터)를 분석하는 전문가입니다. 주어진 헤더 목록을 보고, 이 엑셀 파일이 어떤 종류의 데이터인지 한 문장으로 명확하게 분류해주세요."
)

# --- 파일 업로드 기능 ---
uploaded_file = st.file_uploader("엑셀 파일을 선택하세요 (.xlsx, .xls)", type=["xlsx", "xls"])

if uploaded_file is not None:
    st.info(f"파일명: {uploaded_file.name} (업로드 완료)")

    # "분류 시작" 버튼
    if st.button("AI로 분류 시작하기"):
        try:
            # --- 핵심 로직: 엑셀 파일의 '첫 번째 행(헤더)'만 읽기 ---
            df_header = pd.read_excel(uploaded_file, nrows=0)
            header_list = df_header.columns.tolist()
            header_text = ", ".join(header_list)

            with st.spinner("AI가 엑셀 파일의 필터를 분석 중입니다..."):
                # AI에게 헤더 텍스트를 보내 질문
                prompt = f"다음은 엑셀 파일의 필터(헤더) 목록입니다: [{header_text}]. 이 엑셀 파일은 어떤 종류의 데이터입니까?"
                response = model.generate_content(prompt)

                # 결과 출력
                st.subheader("AI 분석 결과 ✨")
                st.success(response.text)

        except Exception as e:
            st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
            st.warning("올바른 엑셀 파일 형식이 맞는지 확인해주세요.")
