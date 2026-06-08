import streamlit as st
import fitz  # PyMuPDF
import spacy
from spacy.matcher import PhraseMatcher
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Skill Analyzer",
    layout="wide"
)

# ---------------- LOAD NLP MODEL ----------------
nlp = spacy.load("en_core_web_sm")

# ---------------- SKILLS DATA ----------------
all_skills = [
    "Python", "Java", "C++", "SQL", "Excel", "Tableau", "Power BI",
    "Machine Learning", "Deep Learning", "NLP", "Cloud Computing",
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Git",
    "SEO", "Content Marketing", "Google Analytics", "Social Media",
    "Email Marketing", "Statistics", "Pandas", "NumPy", "TensorFlow",
    "PyTorch", "JavaScript", "React", "Node.js", "HTML", "CSS",
    "UI/UX Design", "Project Management", "Agile", "Scrum",
    "Leadership", "Communication"
]

trending_skills = {
    "Software Engineer": ["Python", "Git", "Docker", "Kubernetes", "Cloud Computing"],
    "Data Analyst": ["SQL", "Excel", "Python", "Statistics", "Power BI"],
    "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "Pandas", "NumPy"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "Digital Marketer": ["SEO", "Content Marketing", "Google Analytics", "Social Media"],
    "Project Manager": ["Project Management", "Agile", "Scrum", "Leadership"]
}

roadmap = {
    "Software Engineer": [
        "DSA Fundamentals",
        "Git & GitHub",
        "Backend Development",
        "Docker & Kubernetes",
        "Cloud Deployment"
    ],
    "Data Scientist": [
        "Python & Statistics",
        "Machine Learning",
        "Deep Learning",
        "Model Deployment"
    ]
}

# 🔥 EXTENDED COURSES LIST
courses = {
    # Programming
    "Python": "https://www.coursera.org/specializations/python",
    "Java": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
    "C++": "https://www.udemy.com/course/beginning-c-plus-plus-programming/",
    "JavaScript": "https://www.udemy.com/course/the-complete-javascript-course/",
    "React": "https://www.udemy.com/course/react-the-complete-guide/",
    "Node.js": "https://www.udemy.com/course/nodejs-the-complete-guide/",
    "HTML": "https://www.coursera.org/learn/html-css-javascript-for-web-developers",
    "CSS": "https://www.coursera.org/learn/html-css-javascript-for-web-developers",

    # Data & Analytics
    "SQL": "https://www.udemy.com/course/the-complete-sql-bootcamp/",
    "Excel": "https://www.coursera.org/learn/excel-essentials",
    "Power BI": "https://www.coursera.org/learn/power-bi",
    "Tableau": "https://www.coursera.org/learn/tableau-data-visualization",
    "Statistics": "https://www.coursera.org/learn/statistics",
    "Pandas": "https://www.coursera.org/learn/python-data-analysis",
    "NumPy": "https://www.coursera.org/learn/python-data-analysis",

    # AI / ML
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "Deep Learning": "https://www.coursera.org/specializations/deep-learning",
    "NLP": "https://www.coursera.org/learn/language-processing",
    "TensorFlow": "https://www.coursera.org/learn/introduction-tensorflow",
    "PyTorch": "https://www.udemy.com/course/pytorch-for-deep-learning/",

    # Cloud & DevOps
    "Cloud Computing": "https://www.coursera.org/learn/cloud-computing-basics",
    "AWS": "https://www.coursera.org/learn/aws-cloud-practitioner-essentials",
    "Azure": "https://www.coursera.org/learn/azure-fundamentals",
    "Google Cloud": "https://www.coursera.org/learn/gcp-fundamentals",
    "Docker": "https://www.udemy.com/course/docker-mastery/",
    "Kubernetes": "https://www.udemy.com/course/kubernetes-mastery/",
    "Git": "https://www.udemy.com/course/git-and-github-bootcamp/",

    # Management & Marketing
    "Project Management": "https://www.coursera.org/learn/project-management",
    "Agile": "https://www.coursera.org/learn/agile-project-management",
    "Scrum": "https://www.udemy.com/course/scrum-certification/",
    "Leadership": "https://www.coursera.org/learn/leadership-skills",
    "SEO": "https://www.coursera.org/learn/seo-fundamentals",
    "Content Marketing": "https://www.coursera.org/learn/content-marketing",
    "Google Analytics": "https://www.coursera.org/learn/google-analytics",
    "Social Media": "https://www.coursera.org/learn/social-media-marketing"
}

# ---------------- NLP MATCHER ----------------
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("SKILLS", [nlp.make_doc(skill) for skill in all_skills])

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    doc = nlp(text)
    matches = matcher(doc)
    return list(set(doc[start:end].text for _, start, end in matches))

def display_skills(skills, color):
    if not skills:
        st.write("None")
        return
    html = ""
    for s in skills:
        html += f"""
        <span style="
        background-color:{color};
        padding:7px 12px;
        margin:4px;
        border-radius:20px;
        display:inline-block;
        color:white;
        font-size:14px;">
        {s}
        </span>
        """
    st.markdown(html, unsafe_allow_html=True)

def resume_feedback(text):
    feedback = []
    text = text.lower()
    if "project" not in text:
        feedback.append("Add academic or real-world projects.")
    if "intern" not in text:
        feedback.append("Mention internships or hands-on experience.")
    if len(text.split()) < 300:
        feedback.append("Resume content is too short.")
    return feedback

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center;'>🤖 AI Resume Skill Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload your resume & get smart career insights 🚀</p>", unsafe_allow_html=True)

st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Navigate", ["Resume Analyzer", "About Project"])

# ---------------- MAIN APP ----------------
if menu == "Resume Analyzer":
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    with col2:
        job_role = st.selectbox("🎯 Target Job Role", list(trending_skills.keys()))

    if uploaded_file and job_role:
        resume_text = extract_text_from_pdf(uploaded_file)
        user_skills = extract_skills(resume_text)
        required_skills = trending_skills[job_role]

        matched_skills = list(set(user_skills) & set(required_skills))
        missing_skills = list(set(required_skills) - set(user_skills))

        st.subheader("✅ Skills Found in Resume")
        display_skills(user_skills, "#2196F3")

        st.subheader("🎯 Skills Matched for Job Role")
        display_skills(matched_skills, "#4CAF50")

        st.subheader("🚀 Skills to Learn")
        display_skills(missing_skills, "#FF5722")

        match_percentage = int((len(matched_skills) / len(required_skills)) * 100)
        st.subheader("📊 Skill Match Score")
        st.progress(match_percentage)
        st.write(f"**Match Percentage:** {match_percentage}%")

        st.subheader("📈 Skill Gap Analysis")
        fig, ax = plt.subplots()
        ax.pie([len(matched_skills), len(missing_skills)],
               labels=["Matched", "Missing"],
               autopct="%1.1f%%",
               startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        st.subheader("📝 Resume Feedback")
        for f in resume_feedback(resume_text):
            st.warning(f)

        if job_role in roadmap:
            st.subheader("🛣 Career Roadmap")
            for step in roadmap[job_role]:
                st.checkbox(step)

        st.subheader("🎓 Learning Resources (Based on Missing Skills)")
        found = False
        for skill in missing_skills:
            if skill in courses:
                st.markdown(f"- **{skill}** → [Learn Here]({courses[skill]})")
                found = True
        if not found:
            st.success("🎉 No courses needed. Your skills already match the role!")

elif menu == "About Project":
    st.subheader("📌 About This Project")
    st.write("""
    This AI-powered system uses **spaCy NLP** to analyze resumes,
    detect skill gaps, visualize progress, and recommend learning paths.
    """)
