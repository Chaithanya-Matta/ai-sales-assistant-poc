import streamlit as st
import requests
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8001")

st.set_page_config(page_title="Sales Assistant", layout="centered")
st.title("🧳 AI Sales Assistant POC")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Call the ReAct-style backend agent
        try:
            response = requests.post(
                f"{FASTAPI_URL}/chat",
                json={"query": prompt}
            )
            result = response.json()
            assistant_reply = result.get("response", str(result))
        except Exception as e:
            assistant_reply = f"⚠️ Error: {e}"

        st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})