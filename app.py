import streamlit as st
from openai import OpenAI
import os

# --- Use Streamlit Secrets (secure) ---
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Streamlit UI ---
st.set_page_config(page_title="Simple AI Chatbot", layout="centered")

st.title("💬 Simple AI Chatbot")
st.write("Ask me anything... (Demo for Bhilwara Students)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Thinking...")

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=st.session_state.messages
            )

            ai_reply = response.choices[0].message.content
            placeholder.write(ai_reply)

            # Save reply
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_reply}
            )

        except Exception as e:
            placeholder.write(f"Error: {str(e)}")
