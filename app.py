import os
import io
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ================= CONFIGURATION =================

load_dotenv()

APP_NAME = "Nexora AI"
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()

st.set_page_config(
    page_title="Nexora AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= CUSTOM CSS =================

st.markdown("""
<style>
/* Main background */
.stApp {
    background: #101116 !important;
    color: #f5f5f7 !important;
}

/* Remove visual effects that can make text unclear */
.stApp * {
    text-shadow: none !important;
    filter: none !important;
}

/* Main text */
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown strong {
    color: #f5f5f7 !important;
    opacity: 1 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #171820 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #f5f5f7 !important;
    opacity: 1 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #191a22 !important;
    border: 1px solid #30313c !important;
    border-radius: 14px !important;
    padding: 16px !important;
    opacity: 1 !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: #f5f5f7 !important;
    opacity: 1 !important;
}

/* Chat input: black text on white background */
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    caret-color: #111111 !important;
    opacity: 1 !important;
    text-shadow: none !important;
    filter: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #555555 !important;
    -webkit-text-fill-color: #555555 !important;
    opacity: 1 !important;
}

/* Other input fields */
.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* Tables */
.stApp table {
    background: #191a22 !important;
    border-collapse: collapse !important;
}

.stApp th,
.stApp td {
    color: #f5f5f7 !important;
    background: #191a22 !important;
    border: 1px solid #383945 !important;
    opacity: 1 !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    background: #272936 !important;
    color: #ffffff !important;
    border: 1px solid #444654 !important;
    border-radius: 10px !important;
}

.stButton button:hover {
    border-color: #8b83ff !important;
}

/* Code blocks */
pre, code {
    opacity: 1 !important;
    filter: none !important;
}

/* Footer */
.nexora-footer {
    text-align: center;
    padding: 20px 5px;
    margin-top: 35px;
    border-top: 1px solid #30313c;
    color: #b8b8c8 !important;
    font-size: 13px;
}

.nexora-brand {
    color: #ffffff !important;
    font-size: 15px;
    font-weight: 700;
}

.nexora-creator {
    color: #bcb4ff !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_number" not in st.session_state:
    st.session_state.chat_number = 1


def clear_chat():
    st.session_state.messages = []
    st.session_state.chat_number += 1


# ================= SIDEBAR =================

with st.sidebar:
    st.markdown("# ✦ Nexora AI")
    st.caption("Your AI assistant")

    if st.button("＋ New Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    if st.button("🗑 Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    st.divider()

    st.markdown("### Features")

    feature = st.radio(
        "Choose a feature",
        [
            "General Chat",
            "Study Help",
            "Coding Assistant",
            "Math Solver",
            "Writing Assistant",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### AI Model")
    st.code(MODEL)

    st.markdown("""
    <div style="text-align:center; padding:12px 0;">
        <div style="color:#bcb4ff; font-size:13px;">
            ✦ Nexora AI
        </div>
        <div style="color:#ffffff; font-size:14px; margin-top:5px;">
            Created by <b>Apan2026</b>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ================= HEADER =================

st.markdown("""
<div style="text-align:center; padding:12px 0 18px 0;">
    <h1 style="color:#ffffff; font-size:38px;">
        ✦ Nexora AI
    </h1>
    <p style="color:#c5c5d0; font-size:16px;">
        Think smarter. Learn faster. Create more.
    </p>
</div>
""", unsafe_allow_html=True)

if feature != "General Chat":
    st.info(f"Selected mode: {feature}")


# ================= FILE ATTACHMENT =================

uploaded_file = st.file_uploader(
    "📎 Attach a file",
    type=[
        "txt", "py", "html", "css", "js",
        "json", "csv", "md", "pdf"
    ],
)

attachment_text = ""

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            try:
                from pypdf import PdfReader

                pdf = PdfReader(io.BytesIO(uploaded_file.getvalue()))

                attachment_text = "\n".join(
                    page.extract_text() or ""
                    for page in pdf.pages
                )

            except ImportError:
                st.warning(
                    "PDF reading needs pypdf. "
                    "Run: python -m pip install pypdf"
                )
        else:
            attachment_text = uploaded_file.getvalue().decode(
                "utf-8", errors="replace"
            )

        st.success(f"Attached: {uploaded_file.name}")

        if attachment_text:
            with st.expander("Preview file"):
                st.text(attachment_text[:3000])

    except Exception as error:
        st.error(f"File error: {error}")


# ================= DISPLAY CHAT HISTORY =================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ================= AI INSTRUCTIONS =================

instructions = {
    "General Chat": (
        "You are Nexora AI, a helpful assistant. "
        "Answer clearly in the language the user uses."
    ),
    "Study Help": (
        "You are Nexora AI, a patient tutor. "
        "Explain concepts step by step with examples."
    ),
    "Coding Assistant": (
        "You are Nexora AI, an expert programming helper. "
        "Provide useful code and explain how to run it."
    ),
    "Math Solver": (
        "You are Nexora AI, a math tutor. "
        "Solve problems step by step and check calculations."
    ),
    "Writing Assistant": (
        "You are Nexora AI, a writing assistant. "
        "Help users write and improve their text."
    ),
}


# ================= CHAT INPUT =================

prompt = st.chat_input("Message Nexora AI...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    if not API_KEY:
        error_message = (
            "GROQ_API_KEY পাওয়া যায়নি। "
            "Nexora AI ফোল্ডারের .env ফাইল পরীক্ষা করো।"
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": error_message,
        })

        with st.chat_message("assistant"):
            st.error(error_message)

    else:
        try:
            client = Groq(api_key=API_KEY)

            api_messages = [{
                "role": "system",
                "content": instructions[feature],
            }]

            for message in st.session_state.messages[-12:]:
                api_messages.append({
                    "role": message["role"],
                    "content": message["content"],
                })

            if attachment_text:
                api_messages[-1]["content"] += (
                    "\n\nAttached file content:\n"
                    + attachment_text[:12000]
                )

            with st.chat_message("assistant"):
                with st.spinner("Nexora AI is thinking..."):
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=api_messages,
                        temperature=0.6,
                        max_tokens=3000,
                    )

                    answer = response.choices[0].message.content
                    answer = answer or "কোনো উত্তর পাওয়া যায়নি।"

                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

        except Exception as error:
            error_message = f"AI request failed: {error}"

            with st.chat_message("assistant"):
                st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
            })


# ================= FOOTER =================

st.markdown("""
<div class="nexora-footer">
    <div class="nexora-brand">✦ Nexora AI</div>
    <div style="margin-top:6px;">
        Created by <span class="nexora-creator">Apan2026</span>
    </div>
    <div style="margin-top:8px; font-size:11px;">
        AI can make mistakes. Verify important information.
    </div>
</div>
""", unsafe_allow_html=True)

