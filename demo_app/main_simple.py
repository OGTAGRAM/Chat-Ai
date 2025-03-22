"""Python file to serve as the frontend"""
import sys
import os
import streamlit as st
import time
import google.generativeai as genai
from demo_app.components.sidebar import sidebar

sys.path.append(os.path.abspath('.'))

def load_gemini_model():
    """Logic for loading the Gemini model."""
    genai.configure(api_key=st.session_state.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.0-flash')
    return model

if __name__ == "__main__":
    st.set_page_config(
        page_title="Chat App: Gemini",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("📖 Chat App: Gemini Demo")
    sidebar()

    if not st.session_state.get("gemini_api_key_configured"):
        st.error("Please configure your Gemini API Keys!")
    else:
        model = load_gemini_model()

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # **UPLOAD FILE SECTION**
        uploaded_files = st.file_uploader("Upload files (optional)", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)
        if uploaded_files:
            st.session_state["uploaded_files"] = uploaded_files
            st.success(f"{len(uploaded_files)} file(s) uploaded.")

        # **CHAT INPUT SECTION**
        user_input = st.chat_input("What is your question?")

        if user_input:
            # Simpan pertanyaan pengguna ke session state
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Tampilkan pesan user
            with st.chat_message("user"):
                st.markdown(user_input)

            # **Tampilkan file yang diunggah**
            if "uploaded_files" in st.session_state and st.session_state["uploaded_files"]:
                for file in st.session_state["uploaded_files"]:
                    st.markdown(f"📎 Uploaded file: `{file.name}`")

            # **PROSES RESPON AI**
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner('CHAT-BOT is at Work ...'):
                    # Siapkan riwayat percakapan untuk Gemini
                    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

                    # Generate response menggunakan Gemini
                    response = model.generate_content(conversation_history)
                    assistant_response = response.text

                # Simulasi output teks bertahap (typing effect)
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # Simpan respons ke dalam sesi percakapan
            st.session_state.messages.append({"role": "assistant", "content": full_response})
