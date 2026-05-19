# app.py

import streamlit as st
import pdfplumber
import re
from collections import Counter

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")

st.write("Upload your resume and analyze your skills using AI-based keyword extraction.")

# Skill database
skills_db = [
    "Python", "SQL", "Machine Learning", "Data Analysis",
    "Power BI", "Excel", "TensorFlow", "Scikit-learn",
    "Pandas", "NumPy", "Matplotlib", "Deep Learning",
    "NLP", "AI", "Git", "GitHub", "MySQL",
    "Data Visualization", "Streamlit"
]

# Function to extract text from PDF
def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text

# Function to extract skills
def extract_skills(text):
    found_skills = []

    for skill in skills_db:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills

# Upload resume
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume Uploaded Successfully!")

    # Extract text
    resume_text = extract_text(uploaded_file)

    # Extract skills
    skills = extract_skills(resume_text)

    st.subheader("✅ Extracted Skills")

    if skills:
        for skill in skills:
            st.write(f"✔ {skill}")
    else:
        st.write("No matching skills found.")

    # Resume Score
    score = len(skills) * 5

    if score > 100:
        score = 100

    st.subheader("📊 Resume Score")

    st.progress(score)

    st.write(f"Your Resume Score: {score}/100")

    # Suggestions
    st.subheader("💡 Suggestions")

    missing_skills = []

    for skill in skills_db:
        if skill not in skills:
            missing_skills.append(skill)

    if missing_skills:
        st.write("Consider adding these skills:")
        st.write(", ".join(missing_skills[:10]))

    # Word Frequency
    words = re.findall(r'\w+', resume_text.lower())

    common_words = Counter(words).most_common(10)

    st.subheader("📈 Most Common Words")

    for word, count in common_words:
        st.write(f"{word} : {count}")