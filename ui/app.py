import json
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="LLM Resume Analyzer",
    layout="wide"
)

st.title("LLM-Powered Resume Analyzer & Job Matcher")
st.write(
    "Upload a resume and paste a job description to get a skill match score, "
    "gap analysis, and learning roadmap."
)

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Inputs")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Looking for an ML Engineer with Python, PyTorch, LangChain..."
    )

    analyze_btn = st.button("Analyze Resume")

def call_api(resume_file, job_description):
    files = {
        "resume": (resume_file.name, resume_file, "application/pdf")
    }
    data = {
        "job_description": job_description
    }
    try:
        response = requests.post(API_URL, files=files, data=data, timeout=120)
    except requests.RequestException as exc:
        return {"error": f"API request failed: {exc}"}

    if response.status_code != 200:
        return {"error": f"API error {response.status_code}: {response.text}"}

    try:
        return response.json()
    except ValueError:
        return {"error": "API returned invalid JSON."}

with col2:
    st.header("Analysis Results")

    if analyze_btn:
        if resume_file is None or not job_description.strip():
            st.warning("Please upload a resume and enter a job description.")
        else:
            with st.spinner("Analyzing resume..."):
                result = call_api(resume_file, job_description)

            if "error" in result:
                st.error(result["error"])
            else:
                analysis = result.get("analysis", {})
                llm = result.get("llm_feedback", {}) or {}
                if isinstance(llm, str):
                    try:
                        llm = json.loads(llm)
                    except json.JSONDecodeError:
                        llm = {"overall_feedback": llm}
                if isinstance(llm, dict):
                    overall_text = llm.get("overall_feedback", "")
                    if isinstance(overall_text, str) and overall_text.strip().startswith("{"):
                        try:
                            parsed = json.loads(overall_text)
                            if isinstance(parsed, dict):
                                llm = parsed
                        except json.JSONDecodeError:
                            pass

                st.subheader("Match Score")
                st.metric("Overall Match (%)", analysis.get("match_score", 0))

                st.subheader("Matched Skills")
                strengths = analysis.get("summary", {}).get("strengths", [])
                if strengths:
                    for skill in strengths:
                        st.write(f"- {skill}")
                else:
                    st.write("No matched skills found.")

                st.subheader("Skill Gaps")
                missing = analysis.get("missing_skills", [])
                if missing:
                    for item in missing:
                        st.write(
                            f"- **{item.get('skill', 'Unknown')}** "
                            f"({item.get('priority', 'Unknown')} Priority)"
                        )
                else:
                    st.write("No missing skills found.")

                st.subheader("AI Feedback")
                st.write(llm.get("overall_feedback", "No LLM feedback available."))

                st.subheader("Learning Roadmap")
                learning = llm.get("learning_roadmap", [])
                if isinstance(learning, str):
                    learning = [learning]
                if learning:
                    for step in learning:
                        st.write(f"- {step}")
                else:
                    st.write("No learning roadmap provided.")
