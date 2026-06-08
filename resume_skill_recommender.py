import streamlit as st
import fitz  # PyMuPDF
import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy English ML model
nlp = spacy.load("en_core_web_sm")

# Curated skills list
all_skills = [
    "Python", "Java", "C++", "SQL", "Excel", "Tableau", "Power BI",
    "Machine Learning", "Deep Learning", "NLP", "Cloud Computing",
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Git",
    "SEO", "Content Marketing", "Google Analytics", "Social Media",
    "Email Marketing", "Statistics", "Pandas", "NumPy", "TensorFlow",
    "PyTorch", "JavaScript", "React", "Node.js", "HTML", "CSS", "UI/UX Design",
    "Project Management", "Agile", "Scrum", "Leadership", "Communication"
]

# ML matcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in all_skills]
matcher.add("SKILLS", patterns)

# Trending skills per role
trending_skills = {
    "Software Engineer": ["Python", "Docker", "Kubernetes", "Machine Learning", "Cloud Computing", "Git"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Python", "Statistics", "Power BI"],
    "Digital Marketer": ["SEO", "Content Marketing", "Google Analytics", "Social Media", "Email Marketing"],
    "Web Developer": ["JavaScript", "React", "Node.js", "HTML", "CSS", "Git"],
    "Project Manager": ["Project Management", "Agile", "Scrum", "Leadership", "Communication"],
    "Data Scientist": ["Python", "R", "Machine Learning", "Deep Learning", "Statistics", "Pandas", "NumPy", "TensorFlow", "PyTorch"],
    "UI/UX Designer": ["UI/UX Design", "Adobe XD", "Figma", "Wireframing", "Prototyping", "User Research"],
}

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ML-based skill extraction
def extract_skills_with_ml(resume_text):
    doc = nlp(resume_text)
    matches = matcher(doc)
    found_skills = [doc[start:end].text for match_id, start, end in matches]
    return list(set(found_skills))

# Recommend missing skills
def recommend_skills(user_skills, job_role):
    required_skills = trending_skills.get(job_role, [])
    recommended = list(set(required_skills) - set(user_skills))
    return recommended

# Streamlit UI
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
        


