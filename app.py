import streamlit as st
from openai import OpenAI
from dialogue_prompts import boy_prompt, girl_prompt

# Load OpenAI Key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="사춘기 중재 대화 챗봇", layout="centered")

st.title("👩‍👧‍👦 사춘기 자녀와 대화하는 엄마 챗봇")
st.markdown("사춘기 **아들 또는 딸과의 갈등 상황**에서, 대화를 통해 공감과 해결을 이끌어보세요.")

# 선택
role = st.selectbox("💬 누구와 대화하시겠습니까?", ["아들", "딸"])

# 대화 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 시스템 역할 설정
if role == "아들":
    system_prompt = boy_prompt
else:
    system_prompt = girl_prompt

# 대화 시작
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": system_prompt})

# 채팅 입력창
user_input = st.chat_input("자녀와의 상황을 말해보세요.")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 대화 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
