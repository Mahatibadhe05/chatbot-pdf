import streamlit as st
from pypdf import PdfReader

st.title("PDF Chatbot")

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

        question = question.lower()

        sentences = text.split(".")

        answer_found = False

        for sentence in sentences:

            if any(word in sentence.lower()
                   for word in question.split()):

                st.subheader("Answer")

                st.write(sentence)

                answer_found = True

                break

        if not answer_found:
            st.write(
                "Sorry, I could not find an answer in the PDF."
            )