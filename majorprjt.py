import streamlit as st
import fitz
import spacy
from spacy.matcher import PhraseMatcher
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Skill Analyzer",
    layout="wide"
)

# ---------------- ADVANCED UI (FRONTEND ONLY) ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #e0eafc, #cfdef3);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Title */
h1 {
    text-align: center;
    color: #0f2027;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.2);
}

/* Glass Card Effect */
.glass {
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    margin-bottom: 20px;
    transition: transform 0.3s ease;
}

.glass:hover {
    transform: translateY(-6px);
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #0072ff, #00c6ff);
    color: white;
    border-radius: 30px;
    padding: 10px 22px;
    border: none;
    box-shadow: 0 8px 18px rgba(0,0,0,0.2);
}
.stButton button:hover {
    transform: scale(1.05);
}

/* File uploader */
.stFileUploader {
    background: rgba(255,255,255,0.6);
    border-radius: 16px;
    padding: 12px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD NLP MODEL ----------------
nlp = spacy.load("en_core_web_sm")

# ---------------- DATA ----------------
all_skills = [
    "Python","Java","C++","SQL","Excel","Tableau","Power BI",
    "Machine Learning","Deep Learning","NLP","Cloud Computing",
    "AWS","Azure","Google Cloud","Docker","Kubernetes","Git",
    "SEO","Content Marketing","Google Analytics","Social Media",
    "Statistics","Pandas","NumPy","TensorFlow","PyTorch",
    "JavaScript","React","Node.js","HTML","CSS",
    "Project Management","Agile","Scrum","Leadership"
]

trending_skills = {
    "Software Engineer": ["Python","Git","Docker","Kubernetes","Cloud Computing"],
    "Data Analyst": ["SQL","Excel","Python","Statistics","Power BI"],
    "Data Scientist": ["Python","Machine Learning","Deep Learning","Pandas","NumPy"],
    "Web Developer": ["HTML","CSS","JavaScript","React","Git"],
    "Digital Marketer": ["SEO","Content Marketing","Google Analytics","Social Media"],
    "Project Manager": ["Project Management","Agile","Scrum","Leadership"]
}

roadmap = {
    "Software Engineer": ["DSA","Git","Backend","Docker","Cloud"],
    "Data Analyst": ["Excel","SQL","Python","Visualization","Reporting"],
    "Data Scientist": ["Statistics","ML","DL","Projects","Deployment"],
    "Web Developer": ["HTML/CSS","JavaScript","React","Backend","Deploy"],
    "Digital Marketer": ["SEO","Content","Analytics","Ads","Optimization"],
    "Project Manager": ["Planning","Agile","Risk","Communication","Delivery"]
}

courses = {
    "Python": "https://www.coursera.org/specializations/python",
    "Java": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
    "C++": "https://www.udemy.com/course/beginning-c-plus-plus-programming/",
    "SQL": "https://www.udemy.com/course/the-complete-sql-bootcamp/",
    "Excel": "https://www.coursera.org/learn/excel-essentials",
    "Tableau": "https://www.coursera.org/learn/data-visualization-tableau",
    "Power BI": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/",
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "Deep Learning": "https://www.coursera.org/specializations/deep-learning",
    "NLP": "https://www.coursera.org/learn/natural-language-processing",
    "Cloud Computing": "https://www.coursera.org/learn/cloud-computing",
    "AWS": "https://www.aws.training/Details/Curriculum?id=20685",
    "Azure": "https://learn.microsoft.com/en-us/training/azure/",
    "Google Cloud": "https://www.coursera.org/professional-certificates/google-cloud",
    "Docker": "https://www.udemy.com/course/docker-mastery/",
    "Kubernetes": "https://www.udemy.com/course/learn-kubernetes/",
    "Git": "https://www.udemy.com/course/git-and-github-bootcamp/",
    "SEO": "https://www.coursera.org/learn/seo",
    "Content Marketing": "https://www.coursera.org/learn/content-marketing",
    "Google Analytics": "https://analytics.google.com/analytics/academy/",
    "Social Media": "https://www.coursera.org/learn/social-media-marketing",
    "Statistics": "https://www.coursera.org/learn/probability-statistics",
    "Pandas": "https://www.datacamp.com/courses/pandas-foundations",
    "NumPy": "https://www.datacamp.com/courses/intro-to-python-for-data-science",
    "TensorFlow": "https://www.coursera.org/learn/deep-learning-tensorflow",
    "PyTorch": "https://www.udemy.com/course/pytorch-for-deep-learning/",
    "JavaScript": "https://www.udemy.com/course/the-complete-javascript-course/",
    "React": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
    "Node.js": "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/",
    "HTML": "https://www.udemy.com/course/html-and-css-for-beginners/",
    "CSS": "https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/",
    "Project Management": "https://www.coursera.org/specializations/project-management",
    "Agile": "https://www.coursera.org/learn/agile-development",
    "Scrum": "https://www.scrum.org/resources/what-is-scrum",
    "Leadership": "https://www.coursera.org/learn/leadership-skills"
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
        background:{color};
        padding:8px 14px;
        margin:5px;
        border-radius:25px;
        display:inline-block;
        color:white;
        font-weight:500;
        box-shadow:0 5px 15px rgba(0,0,0,0.2);">
        {s}
        </span>
        """
    st.markdown(html, unsafe_allow_html=True)

def resume_feedback(text):
    fb=[]
    text=text.lower()
    if "project" not in text: fb.append("Add projects")
    if "intern" not in text: fb.append("Add internship experience")
    if len(text.split())<300: fb.append("Resume is too short")
    return fb

# ---------------- UI ----------------
st.markdown("<h1>AI Resume Skill Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart • Visual • Career-Ready </p>", unsafe_allow_html=True)

st.sidebar.title(" Navigation")
menu = st.sidebar.radio("Menu", ["Resume Analyzer","About Project"])

# ---------------- MAIN ----------------
if menu=="Resume Analyzer":

    col1,col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    with col2:
        job_role = st.selectbox(" Target Role", list(trending_skills.keys()))

    if uploaded_file and job_role:
        resume_text = extract_text_from_pdf(uploaded_file)
        user_skills = extract_skills(resume_text)
        required = trending_skills[job_role]

        matched = list(set(user_skills)&set(required))
        missing = list(set(required)-set(user_skills))

        st.markdown("<div class='glass'><h3> Skills Found</h3></div>", unsafe_allow_html=True)
        display_skills(user_skills,"#0072ff")

        st.markdown("<div class='glass'><h3> Matched Skills</h3></div>", unsafe_allow_html=True)
        display_skills(matched,"#00b894")

        st.markdown("<div class='glass'><h3> Skills to Learn</h3></div>", unsafe_allow_html=True)
        display_skills(missing,"#ff7675")

        score=int((len(matched)/len(required))*100)
        st.markdown("<div class='glass'><h3> Match Score</h3></div>", unsafe_allow_html=True)
        st.progress(score)
        st.write(f"**{score}% Match**")

        fig,ax=plt.subplots()
        ax.pie([len(matched),len(missing)],labels=["Matched","Missing"],autopct="%1.1f%%")
        st.pyplot(fig)

        st.markdown("<div class='glass'><h3> Feedback</h3></div>", unsafe_allow_html=True)
        for f in resume_feedback(resume_text):
            st.warning(f)

        st.markdown("<div class='glass'><h3> Roadmap</h3></div>", unsafe_allow_html=True)
        for step in roadmap[job_role]:
            st.checkbox(step)

        st.markdown("<div class='glass'><h3> Courses</h3></div>", unsafe_allow_html=True)
        for skill in missing:
            if skill in courses:
                st.markdown(f"- **{skill}** → [Learn]({courses[skill]})")

else:
    st.write("AI powered resume analyzer with 3D-style UI and skill intelligence.")

