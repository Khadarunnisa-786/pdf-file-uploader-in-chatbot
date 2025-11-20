import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import tempfile

# --- Load API key ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Missing GOOGLE_API_KEY in your .env file.")
else:
    genai.configure(api_key=api_key)

# --- Initialize the Gemini model ---
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Streamlit page setup ---
st.set_page_config(page_title="Chat with PDF - Gemini", page_icon="📄", layout="centered")
st.title("📘 Chat with PDF using Gemini 2.0 Flash")

st.markdown("""
Upload a **PDF document**, and ask Gemini to **summarize or answer questions** based on it.  
Works with the **latest Google Generative AI SDK (v1.x)**.
""")

# --- File uploader ---
uploaded_file = st.file_uploader("📂 Upload a PDF", type=["pdf"])

# --- Session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file:
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Input box for questions
    user_prompt = st.text_input("💬 Ask something about the PDF", placeholder="e.g. Summarize this document or Explain chapter 2...")

    if st.button("Ask Gemini") and user_prompt:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        with st.spinner("Generating response... ⏳"):
            try:
                response = model.generate_content(
                    [user_prompt, {"mime_type": "application/pdf", "data": pdf_bytes}]
                )

                answer = response.text
                st.session_state.chat_history.append(("🧑‍💻 You", user_prompt))
                st.session_state.chat_history.append(("🤖 Gemini", answer))

                st.success("✅ Done!")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("🗨️ Chat History")
        for sender, msg in st.session_state.chat_history:
            if sender == "🧑‍💻 You":
                st.markdown(f"**{sender}:** {msg}")
            else:
                st.markdown(f"<div style='background-color:#f1f1f1;padding:10px;border-radius:8px'><b>{sender}:</b> {msg}</div>", unsafe_allow_html=True)

else:
    st.info("📤 Please upload a PDF to begin.")

