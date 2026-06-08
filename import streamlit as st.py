import streamlit as st
import fitz  # PyMuPDF
import spacy

# Load spaCy's English NLP model (this is pre-trained ML)
nlp = spacy.load("en_core_web_sm")

# Mock trending skills
trending_skills = {
    "Software Engineer": ["Python", "Docker", "Kubernetes", "Machine Learning", "Cloud Computing", "Git"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Python", "Statistics", "Power BI"],
    "Digital Marketer": ["SEO", "Content Marketing", "Google Analytics", "Social Media", "Email Marketing"]
}

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills_with_ml(resume_text):
    doc = nlp(resume_text)
    found_skills = []

    # Use simple rule: treat PROPN, NOUN chunks as possible skills
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "TECHNOLOGY"]:
            found_skills.append(ent.text)
    # Also add noun chunks that look like skills
    for chunk in doc.noun_chunks:
        if chunk.text.istitle():
            found_skills.append(chunk.text)
    return list(set([s.strip() for s in found_skills]))

def recommend_skills(user_skills, job_role):
    required_skills = trending_skills.get(job_role, [])
    recommended = list(set(required_skills) - set(user_skills))
    return recommended

st.title("🤖 ML-powered Job Skill Recommendation System")
st.write("Upload your resume — get smart skill suggestions using NLP!")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

job_role = st.selectbox(
    "Select your target job role:",
    list(trending_skills.keys())
)

if uploaded_file and job_role:
    resume_text = extract_text_from_pdf(uploaded_file)
    user_skills = extract_skills_with_ml(resume_text)

    st.subheader("✅ Skills Found in Resume (ML Extracted):")
    if user_skills:
        st.write(user_skills)
    else:
        st.write("No skills/entities detected.")

    recommended = recommend_skills(user_skills, job_role)

    st.subheader("🚀 Recommended Skills to Learn:")
    if recommended:
        st.write(recommended)
    else:
        st.write("Awesome! You have all trending skills for this role. 🎉")
