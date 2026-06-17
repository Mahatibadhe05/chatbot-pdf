import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6INLCbKoLpnIf8bYBFOrydyAkk2A-Ol1sdhqAN7WlKPQg")

model = genai.GenerativeModel("gemini-2.0-flash")

st.title("AI PDF Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    st.success("PDF uploaded successfully!")

    question = st.text_input(
        "Ask a question about the PDF"
    )

    if question:

        prompt = f"""
        Answer the question ONLY using the information
        present in the PDF below.

        PDF:
        {text}

        Question:
        {question}
        """

        response = model.generate_content(prompt)

        st.subheader("Answer")

        st.write(response.text)