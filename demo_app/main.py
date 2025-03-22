"""Python file to serve as the frontend"""
import sys
import os
sys.path.append(os.path.abspath('.'))

import streamlit as st
import time
import tempfile
import google.generativeai as genai
print(genai.__version__)
from demo_app.components.sidebar import sidebar
from langchain_community.document_loaders import PyPDFLoader

def load_gemini_model():
    """Logic for loading the Gemini model."""
    genai.configure(api_key=st.session_state.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.0-flash')
    return model

def process_pdf(uploaded_file):
    """Process the PDF file and return its content."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    pages = loader.load()
    pdf_text = ""
    for page in pages:
        pdf_text += page.page_content + "\n\n"

    os.unlink(tmp_path)
    return pdf_text

def get_response_with_pdf_context(model, query, pdf_content, history):
    """Get response from Gemini with PDF content as context."""
    prompt = f"""You are a helpful assistant that answers questions based on the provided context.

    Context from PDF:
    {pdf_content}

    Conversation History:
    {history}

    Human: {query}

    Assistant:"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    st.set_page_config(
        page_title="Chat App: Gemini",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("📖 Chat App: Gemini")
    sidebar()

    if not st.session_state.get("gemini_api_key_configured"):
        st.error("Please configure your Gemini API Keys!")
    else:
        model = load_gemini_model()

        if "pdf_content" not in st.session_state:
            st.session_state["pdf_content"] = ""

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you? You can upload a PDF document, and I'll use its content to provide better answers."}
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input("What is your question?", accept_file=st.session_state["file_selection"], file_type=["pdf"])

        if user_input:
            pdf_uploaded = False
            query = user_input.text if hasattr(user_input, 'text') else user_input

            if hasattr(user_input, 'files') and user_input.files:
                uploaded_files = user_input.files
                all_pdf_content = ""
                processed_files = []

                for uploaded_file in uploaded_files:
                    if uploaded_file.name.lower().endswith('.pdf'):
                        processed_files.append(uploaded_file.name)
                        with st.spinner(f'Processing PDF: {uploaded_file.name}...'):
                            pdf_content = process_pdf(uploaded_file)
                            all_pdf_content += f"\n\n=== Content from: {uploaded_file.name} ===\n\n{pdf_content}"
                            pdf_uploaded = True

                if processed_files:
                    file_names = ", ".join(processed_files)
                    st.session_state.messages.append({"role": "user", "content": f"Uploaded PDFs: {file_names}"})
                    with st.chat_message("user"):
                        st.markdown(f"Uploaded PDFs: {file_names}")

                    st.session_state["pdf_content"] = all_pdf_content

                    with st.chat_message("assistant"):
                        st.markdown(f"PDF processed successfully. You can now ask questions about the content of {uploaded_file.name}.")
                    st.session_state.messages.append({"role": "assistant", "content": f"PDF processed successfully. You can now ask questions about the content of {uploaded_file.name}."})

            if query:
                st.session_state.messages.append({"role": "user", "content": query})
                with st.chat_message("user"):
                    st.markdown(query)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    with st.spinner('CHAT-BOT is at Work ...'):
                        history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages[:-1]]) # all messages except the last one
                        assistant_response = get_response_with_pdf_context(model, query, st.session_state["pdf_content"], history)

                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})