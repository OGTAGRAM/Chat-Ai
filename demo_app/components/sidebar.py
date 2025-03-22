import streamlit as st
import google.generativeai as genai

from demo_app.components.faq import faq

def set_gemini_api_key(api_key: str):
    st.session_state["GEMINI_API_KEY"] = api_key
    st.session_state["gemini_api_key_configured"] = True
    genai.configure(api_key=api_key)  # Konfigurasi Gemini API
    print('GEMINI API key is Configured Successfully!')

def sidebar():    
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [Google Gemini API key](https://makersuite.google.com/app/apikey) below🔑\n"
        )
        gemini_api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Paste your API key here (AIza...)",
            help="You can get your API key from https://makersuite.google.com/app/apikey.",
            value=st.session_state.get("GEMINI_API_KEY", ""),
        )

        if gemini_api_key_input:
            set_gemini_api_key(gemini_api_key_input)

        if not st.session_state.get("gemini_api_key_configured"):
            st.error("Please configure your Gemini API key!")
        else:
            st.markdown("✅ Gemini API Key Configured!")

        # Dropdown untuk memilih opsi unggah file
        file_selection = st.selectbox(
            "Choose file upload option:",
            options=["No files", "Single", "Multiple"],
            index=0,  # Default ke "No files"
            help="Select whether you want to upload no files, a single file, or multiple files"
        )

        selection_map = {"No files": False, "Single": True, "Multiple": 'multiple'}
        st.session_state["file_selection"] = selection_map[file_selection]

        # Handle unggahan file berdasarkan pilihan
        if file_selection == "Single":
            uploaded_file = st.file_uploader("Upload a file", type=None)
            if uploaded_file is not None:
                st.session_state["uploaded_files"] = [uploaded_file]
                st.success(f"File uploaded: {uploaded_file.name}")
        elif file_selection == "Multiple":
            uploaded_files = st.file_uploader("Upload files", type=None, accept_multiple_files=True)
            if uploaded_files:
                st.session_state["uploaded_files"] = uploaded_files
                st.success(f"{len(uploaded_files)} files uploaded")
        else:
            st.session_state["uploaded_files"] = []

        st.markdown("---")

        # Panggil FAQ
        faq()