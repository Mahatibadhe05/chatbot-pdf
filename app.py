import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import os
import json
import uuid

# =========================
# GEMINI API KEY
# =========================

genai.configure(api_key="AQ.Ab8RN6INLCbKoLpnIf8bYBFOrydyAkk2A-Ol1sdhqAN7WlKPQg")

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# CHAT STORAGE
# =========================

CHAT_DIR = "chats"
os.makedirs(CHAT_DIR, exist_ok=True)


def save_chat(chat_id, messages):
    with open(
        f"{CHAT_DIR}/{chat_id}.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            messages,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_chat(chat_id):

    path = f"{CHAT_DIR}/{chat_id}.json"

    if os.path.exists(path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    return []


def get_chats():

    chats = []

    for file in os.listdir(CHAT_DIR):

        if file.endswith(".json"):

            chat_id = file[:-5]

            try:

                messages = load_chat(chat_id)

                if len(messages) > 0:
                    title = messages[0]["content"][:25]
                else:
                    title = "New Chat"

            except:
                title = "New Chat"

            chats.append(
                {
                    "id": chat_id,
                    "title": title
                }
            )

    chats.reverse()

    return chats


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

# =========================
# SESSION STATE
# =========================

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("📚 Chats")

    if st.button("➕ New Chat"):

        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.messages = []

        st.rerun()

    st.divider()

    chats = get_chats()

    for chat in chats:

        if st.button(
            f"📄 {chat['title']}",
            use_container_width=True
        ):

            st.session_state.chat_id = chat["id"]

            st.session_state.messages = load_chat(
                chat["id"]
            )

            st.rerun()

# =========================
# MAIN PAGE
# =========================

st.title("🤖 AI PDF Chatbot")

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    save_chat(
        st.session_state.chat_id,
        st.session_state.messages
    )

    st.rerun()

# =========================
# PDF UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "📄 Upload a PDF",
    type="pdf"
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    st.session_state.pdf_text = text

    st.success("✅ PDF uploaded successfully!")

# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================

question = st.chat_input("Ask anything...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    save_chat(
        st.session_state.chat_id,
        st.session_state.messages
    )

    with st.chat_message("user"):
        st.markdown(question)

    try:

        history = ""

        for msg in st.session_state.messages:

            history += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        prompt = f"""
You are a friendly AI assistant.

If the user asks about the uploaded PDF,
use the PDF as your primary source.

If the answer is available in the PDF,
answer using the PDF.

If the user is chatting normally,
respond naturally like ChatGPT.

If information is not available in the PDF,
you may answer using your own knowledge.

PDF CONTENT:
{st.session_state.pdf_text[:30000]}

CHAT HISTORY:
{history}

CURRENT USER MESSAGE:
{question}
"""

        response = model.generate_content(prompt)

        answer = response.text

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        save_chat(
            st.session_state.chat_id,
            st.session_state.messages
        )

    except Exception as e:

        with st.chat_message("assistant"):
            st.error(f"Error: {e}")