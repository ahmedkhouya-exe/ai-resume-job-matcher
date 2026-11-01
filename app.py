"""Streamlit UI for the AI Resume & Job Matcher."""
from __future__ import annotations
from pathlib import Path
import io
import streamlit as st
from matcher import analyze_match

st.set_page_config(page_title="AI Resume & Job Matcher", page_icon="🎯", layout="wide")
st.title("🎯 AI Resume & Job Matcher")
st.markdown("Compare a resume with a job description, explore text similarity, and identify skills to highlight or develop.")
st.caption("Transparent NLP demo · Python · scikit-learn · Streamlit")


def extract_uploaded_text(upload) -> str:
    """Extract selectable text from supported resume formats."""
    suffix, raw = Path(upload.name).suffix.lower(), upload.getvalue()
    if suffix == ".txt":
        return raw.decode("utf-8", errors="replace")
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        from docx import Document
        doc = Document(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type. Upload TXT, PDF, or DOCX.")

with st.container(border=True):
    st.subheader("1. Add your resume")
    upload = st.file_uploader("Upload a TXT, PDF, or DOCX resume (optional)", type=["txt", "pdf", "docx"])
    resume_text = st.text_area("Or paste resume text here", height=220, placeholder="Paste your resume text: experience, projects, education, skills...", help="Pasted text takes priority over uploaded content.")
    if upload is not None and not resume_text.strip():
        try:
            resume_text = extract_uploaded_text(upload)
            if resume_text.strip(): st.success(f"Resume text extracted from {upload.name}.")
            else: st.warning("No selectable text was found. For scanned PDFs, paste the text manually.")
        except Exception as exc:
            st.error(f"Couldn't read that file ({type(exc).__name__}). Try a TXT file or paste the text directly.")

with st.container(border=True):
    st.subheader("2. Add the job description")
    job_description = st.text_area("Job description", height=220, placeholder="Paste the full job description, including responsibilities and required skills...")

if st.button("Analyze match", type="primary", use_container_width=True):
    if not resume_text.strip() or not job_description.strip():
        st.error("Please provide both resume text and a job description.")
    else:
        try:
            result = analyze_match(resume_text, job_description)
            st.divider(); st.header("3. Your results")
            a,b,c = st.columns(3)
            a.metric("Overall match estimate", f"{result.match_score}%")
            b.metric("Text similarity", f"{result.text_similarity:.1f}%")
            c.metric("Detected skill coverage", f"{result.skill_coverage:.1f}%" if result.job_skills else "N/A")
            st.progress(result.match_score / 100, text="Overall match estimate (heuristic, not a hiring probability)")
            st.info(result.summary)
            left,right=st.columns(2)
            with left:
                st.subheader("✅ Matching skills")
                st.write("\n".join(f"- {s}" for s in result.matched_skills) if result.matched_skills else "No skills from the built-in list matched yet.")
            with right:
                st.subheader("🧭 Skills not detected in your resume")
                st.write("\n".join(f"- {s}" for s in result.missing_skills) if result.missing_skills else "No missing skills detected from the built-in list.")
                if result.missing_skills: st.caption("Only add skills if you genuinely have them; never invent experience.")
            with st.expander("See all detected skills and scoring method"):
                st.write("**Skills detected in resume:**", ", ".join(result.resume_skills) or "None detected")
                st.write("**Skills detected in job description:**", ", ".join(result.job_skills) or "None detected")
                st.markdown("**Scoring method:** 60% TF-IDF cosine similarity + 40% detected required-skill coverage. If no supported skills are detected in the job description, score falls back to text similarity.")
        except ValueError as exc:
            st.error(str(exc))
st.divider()
st.caption("Privacy: analysis runs in this app session; this project does not intentionally store resume text. Avoid uploading sensitive personal information to public demos. The score is a rough text-based aid, not a hiring decision.")
