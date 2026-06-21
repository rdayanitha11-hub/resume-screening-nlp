import streamlit as st
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------- Extract ----------
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# ---------- Clean ----------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text


# ---------- Streamlit UI ----------
st.title("📄 AI Resume Screening System")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description")

if st.button("Check Match"):

    if resume_file and jd_text:

        resume_text = extract_text_from_pdf(resume_file)
        resume_text = clean_text(resume_text)
        jd_text = clean_text(jd_text)

        docs = [resume_text, jd_text]

        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(docs)

        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100

        st.subheader("Match Score")
        st.write(f"{score:.2f}%")

        if score > 70:
            st.success("HIGH MATCH ✔")
        elif score > 40:
            st.warning("MEDIUM MATCH ⚠")
        else:
            st.error("LOW MATCH ❌")

    else:
        st.warning("Please upload resume and job description")