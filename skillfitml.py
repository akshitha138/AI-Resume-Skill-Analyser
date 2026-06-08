import streamlit as st
import fitz  # PyMuPDF
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# ==============================
# Load spaCy
# ==============================
nlp = spacy.load("en_core_web_sm")

# ==============================
# Mock trending skills (expandable)q
# ==============================
trending_skills = {
    "Software Engineer": ["Python", "Docker", "Kubernetes", "Machine Learning", "Cloud Computing", "Git"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Python", "Statistics", "Power BI"],
    "Digital Marketer": ["SEO", "Content Marketing", "Google Analytics", "Social Media", "Email Marketing"]
}

# Flatten skill list for filtering
global_skills = set(skill for skills in trending_skills.values() for skill in skills)

# ==============================
# STEP 1: Training dataset (toy)
# ==============================
skill_terms = ["Python", "SQL", "Excel", "Docker", "Kubernetes", "SEO", "Git", "Machine Learning"]
non_skill_terms = ["Team", "Work", "Project", "Experience", "Company", "Communication", "Responsibilities"]

X_train = skill_terms + non_skill_terms
y_train = [1] * len(skill_terms) + [0] * len(non_skill_terms)

# Vectorizer
vectorizer = CountVectorizer(lowercase=True)
X_vectors = vectorizer.fit_transform(X_train)

# Train Logistic Regression model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_vectors, y_train)

# ==============================
# STEP 2: PDF text extractor
# ==============================
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ==============================
# STEP 3: ML-based skill extraction
# ==============================
def extract_skills_with_ml(resume_text):
    doc = nlp(resume_text)

    found_skills = []

    # First check single words
    for token in doc:
        if token.is_alpha and len(token.text) > 2:
            word = token.text
            X_test = vectorizer.transform([word])
            pred = clf.predict(X_test)[0]
            if pred == 1 and word in global_skills:
                found_skills.append(word)

    # Then check for multi-word skills (like Machine Learning, Content Marketing)
    for skill in global_skills:
        if " " in skill and skill.lower() in resume_text.lower():
            found_skills.append(skill)

    return list(set(found_skills))

# ==============================
# STEP 4: Recommend skills
# ==============================
def recommend_skills(user_skills, job_role):
    required_skills = trending_skills.get(job_role, [])
    recommended = list(set(required_skills) - set(user_skills))
    return recommended

# ==============================
# Streamlit UI
# ==============================
st.title("🤖 ML-powered Resume Skill Extractor")
st.success("App is running! Upload a PDF to test.")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

job_role = st.selectbox(

    
    "🎯 Select your target job role:",
    list(trending_skills.keys())
)

if uploaded_file and job_role:
    resume_text = extract_text_from_pdf(uploaded_file)
    user_skills = extract_skills_with_ml(resume_text)

    st.subheader("✅ Skills Found in Resume:")
    if user_skills:
        st.write(user_skills)
    else:
        st.warning("No skills detected. Try with a richer resume.")

    recommended = recommend_skills(user_skills, job_role)

    st.subheader("🚀 Recommended Skills to Learn:")
    if recommended:
        st.write(recommended)
    else:
        st.success("Awesome! You already have trending skills for this role 🎉")
        
