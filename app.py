# app.py

import streamlit as st
from main import agent

st.set_page_config(page_title="Travel Assistant", page_icon="✈️", layout="centered")

st.markdown(
    """
    <style>
        .stTextInput > div > div > input {
            font-size: 16px;
            padding: 12px;
        }
        .chat-box {
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 10px;
        }
        .user-msg {
            background-color: #DCF8C6;
            text-align: right;
        }
        .bot-msg {
            background-color: #F1F0F0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI Travel Assistant")
st.markdown(
    "Type your travel questions below"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Ask me about flights or travel policies...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    with st.spinner("Let me check..."):
        reply = agent.run(user_input)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", reply))

# Display chat history
st.markdown("Chat")
for speaker, msg in reversed(st.session_state.chat_history):
    css_class = "chat-box bot-msg" if speaker == "bot" else "chat-box user-msg"
    st.markdown(f'<div class="{css_class}">{msg}</div>', unsafe_allow_html=True)
