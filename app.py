"""Polished Streamlit UI for the AI Resume & Job Matcher."""
from __future__ import annotations

from pathlib import Path
import html
import io

import streamlit as st
from matcher import analyze_match

st.set_page_config(page_title="TalentLens | Resume Matcher", page_icon="🎯", layout="wide")

st.markdown("""
<style>
.stApp {background:#f5f7fc;color:#17233d}
.block-container {max-width:1240px;padding-top:2rem;padding-bottom:3rem}
[data-testid="stHeader"] {background:rgba(245,247,252,.9)}
[data-testid="stSidebar"] {background:#101a31}
[data-testid="stSidebar"] * {color:#e2e8f0}
[data-testid="stSidebar"] hr {border-color:rgba(255,255,255,.14)}
.brand {display:flex;align-items:center;gap:.7rem;font-weight:800;font-size:1.15rem;margin-bottom:1.4rem}
.brand-mark {display:inline-flex;width:2.35rem;height:2.35rem;align-items:center;justify-content:center;border-radius:.8rem;color:white;background:linear-gradient(135deg,#6366f1,#06b6d4);font-size:1.25rem}
.hero {padding:1.8rem 2rem;border-radius:1.35rem;background:linear-gradient(115deg,#111b35,#243b72 62%,#155e75);color:white;margin:.3rem 0 1.5rem;box-shadow:0 18px 45px rgba(30,58,138,.14)}
.hero-kicker {font-size:.75rem;font-weight:750;letter-spacing:.12em;text-transform:uppercase;color:#a5f3fc;margin-bottom:.7rem}
.hero h1 {color:white;font-size:clamp(1.8rem,3vw,2.65rem);line-height:1.12;letter-spacing:-.045em;margin:0 0 .75rem}
.hero p {color:#dbeafe;max-width:700px;margin:0;font-size:1rem;line-height:1.65}
.hero-tags {display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1.25rem}
.hero-tag {font-size:.76rem;padding:.35rem .65rem;border:1px solid rgba(255,255,255,.2);border-radius:99px;color:#f1f5f9;background:rgba(255,255,255,.07)}
.section-heading {font-size:1.1rem;font-weight:750;letter-spacing:-.02em;color:#17233d;margin:.3rem 0 .25rem}
.section-sub {color:#64748b;font-size:.88rem;margin-bottom:1rem}
[data-testid="stVerticalBlockBorderWrapper"] {border-color:#e4eaf4!important;border-radius:1rem!important;background:rgba(255,255,255,.9);box-shadow:0 5px 18px rgba(15,23,42,.025)}
[data-testid="stTextArea"] textarea {border-radius:.8rem;border-color:#dbe3ef;background:#fbfcff;font-size:.92rem;line-height:1.55}
[data-testid="stFileUploader"] section {border-radius:.8rem;border-color:#cbd5e1;background:#f8faff}
.stButton>button[kind="primary"] {border:0;border-radius:.8rem;padding:.7rem 1rem;font-weight:750;background:linear-gradient(100deg,#4f46e5,#0891b2);box-shadow:0 8px 18px rgba(79,70,229,.18)}
.stButton>button {border-radius:.75rem;font-weight:650}
.metric-card {height:100%;min-height:125px;padding:1.05rem 1.15rem;background:white;border:1px solid #e4eaf4;border-radius:1rem;box-shadow:0 5px 18px rgba(15,23,42,.025)}
.metric-label {color:#64748b;font-size:.82rem;font-weight:650;margin-bottom:.55rem}
.metric-value {color:#17233d;font-size:2rem;line-height:1;font-weight:800;letter-spacing:-.05em}
.metric-note {color:#64748b;font-size:.76rem;margin-top:.55rem}
.score-wrap {display:flex;align-items:center;gap:1.25rem;padding:1.35rem;border-radius:1rem;background:linear-gradient(110deg,#eef2ff,#ecfeff);border:1px solid #dbeafe;margin:.5rem 0 1rem}
.score-ring {width:112px;height:112px;flex:0 0 112px;display:flex;align-items:center;justify-content:center;border-radius:50%}
.score-inner {width:86px;height:86px;border-radius:50%;background:white;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:inset 0 0 0 1px #e2e8f0}
.score-number {font-size:1.65rem;line-height:1;font-weight:850;color:#17233d;letter-spacing:-.05em}
.score-small {color:#64748b;font-size:.65rem;margin-top:.2rem}
.score-title {font-size:1.1rem;font-weight:800;color:#17233d;margin-bottom:.35rem}
.score-copy {font-size:.87rem;color:#475569;line-height:1.55}
.skill-list {display:flex;flex-wrap:wrap;gap:.45rem;margin:.6rem 0 .3rem}
.skill-pill {display:inline-block;padding:.4rem .65rem;border-radius:99px;font-size:.8rem;font-weight:650;border:1px solid}
.skill-good {background:#ecfdf5;border-color:#a7f3d0;color:#047857}
.skill-missing {background:#fff7ed;border-color:#fed7aa;color:#c2410c}
.empty-state {padding:1rem;border:1px dashed #cbd5e1;border-radius:.8rem;background:#f8fafc;color:#64748b;font-size:.88rem}
.privacy-note {color:#64748b;font-size:.78rem;line-height:1.55;padding:.8rem 0}
@media(max-width:700px){.block-container{padding:1rem .8rem 2rem}.hero{padding:1.35rem;border-radius:1rem}.score-wrap{flex-direction:column;align-items:flex-start}}
</style>
""", unsafe_allow_html=True)


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
        document = Document(io.BytesIO(raw))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError("Unsupported file type. Upload TXT, PDF, or DOCX.")


def skill_pills(skills: list[str], kind: str, empty_message: str) -> str:
    if not skills:
        return f'<div class="empty-state">{html.escape(empty_message)}</div>'
    css_class = "skill-good" if kind == "good" else "skill-missing"
    pills = "".join(f'<span class="skill-pill {css_class}">{html.escape(skill)}</span>' for skill in skills)
    return f'<div class="skill-list">{pills}</div>'


with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">✦</span> TalentLens</div>', unsafe_allow_html=True)
    st.markdown("### Your workflow")
    st.markdown("**01**  Add your resume")
    st.markdown("**02**  Paste a target role")
    st.markdown("**03**  Review your match")
    st.divider()
    st.markdown("### What gets analyzed?")
    st.markdown("- Text similarity using TF-IDF\n- Skills found in both texts\n- Job skills not detected in the resume")
    st.divider()
    st.markdown("### Built with")
    st.markdown("Python · Streamlit · scikit-learn")
    st.caption("A portfolio project by Ahmed Khouya")
    st.markdown('<p class="privacy-note">Resume text is analyzed during the current app session. This project does not intentionally save submitted resume content. Avoid using sensitive personal data in public demos.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-kicker">AI-powered career toolkit</div>
  <h1>Make your next application<br>more intentional.</h1>
  <p>Compare your resume with a job description, understand the overlap, and spot skills you may want to highlight — all in one clear dashboard.</p>
  <div class="hero-tags">
    <span class="hero-tag">✦ Explainable matching</span>
    <span class="hero-tag">⌁ Skill gap insights</span>
    <span class="hero-tag">↗ Resume analysis</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">Build your match report</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Add both pieces of text to get a transparent, explainable comparison.</div>', unsafe_allow_html=True)

sample_resume_path = Path(__file__).parent / "examples" / "sample_resume.txt"
sample_job_path = Path(__file__).parent / "examples" / "sample_job_description.txt"
sample_resume = sample_resume_path.read_text(encoding="utf-8") if sample_resume_path.exists() else ""
sample_job = sample_job_path.read_text(encoding="utf-8") if sample_job_path.exists() else ""

action_col, hint_col = st.columns([1, 2])
with action_col:
    if st.button("✦ Load sample data", use_container_width=True):
        st.session_state["resume_input"] = sample_resume
        st.session_state["job_input"] = sample_job
        st.session_state["match_result"] = None
with hint_col:
    st.caption("New here? Load the example resume and job description to try the app instantly.")

resume_col, job_col = st.columns(2, gap="large")
with resume_col:
    with st.container(border=True):
        st.markdown("#### 01 · Your resume")
        st.caption("Upload a file or paste the text below.")
        upload = st.file_uploader("Resume file", type=["txt", "pdf", "docx"], help="Supported: TXT, PDF and DOCX. Scanned PDFs may not contain extractable text.", key="resume_upload")
        resume_text = st.text_area("Resume content", height=260, placeholder="Paste your summary, experience, education, projects and skills...", key="resume_input")
        if upload is not None and not resume_text.strip():
            try:
                resume_text = extract_uploaded_text(upload)
                if not resume_text.strip():
                    st.warning("No selectable text found. If this is a scanned PDF, paste its text manually.")
            except Exception as exc:
                st.error(f"Could not read this file ({type(exc).__name__}). Try another file or paste the text.")
                resume_text = ""

with job_col:
    with st.container(border=True):
        st.markdown("#### 02 · Target job")
        st.caption("Paste the full job posting for a more useful comparison.")
        job_description = st.text_area("Job description", height=320, placeholder="Paste the role summary, responsibilities, required skills and qualifications...", key="job_input")
        st.markdown('<div class="privacy-note">Tip: include the required skills section as well as the responsibilities.</div>', unsafe_allow_html=True)

analyze_col, note_col = st.columns([1, 2])
with analyze_col:
    analyze_clicked = st.button("✦ Analyze my match", type="primary", use_container_width=True)
with note_col:
    st.caption("Your score is a text-based estimate, not a hiring probability or a guarantee of job suitability.")

if analyze_clicked:
    if not resume_text.strip():
        st.error("Please upload a resume or paste your resume text.")
        st.session_state["match_result"] = None
    elif not job_description.strip():
        st.error("Please paste the target job description.")
        st.session_state["match_result"] = None
    else:
        try:
            st.session_state["match_result"] = analyze_match(resume_text, job_description)
        except ValueError as exc:
            st.error(str(exc))
            st.session_state["match_result"] = None

result = st.session_state.get("match_result")
if result is not None:
    st.divider()
    st.markdown('<div class="section-heading">Your match report</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Use these insights to review how clearly your experience maps to the role.</div>', unsafe_allow_html=True)
    score = int(result.match_score)
    ring_degrees = score * 3.6
    st.markdown(f"""
    <div class="score-wrap">
      <div class="score-ring" style="background:conic-gradient(#4f46e5 0deg,#0891b2 {ring_degrees}deg,#dbeafe {ring_degrees}deg,#dbeafe 360deg)">
        <div class="score-inner"><div class="score-number">{score}%</div><div class="score-small">match estimate</div></div>
      </div>
      <div><div class="score-title">Your resume-to-role snapshot</div><div class="score-copy">{html.escape(result.summary)}<br><br>This is an approximate text-based signal. It cannot judge your full experience, context, potential or suitability.</div></div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="medium")
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Text similarity</div><div class="metric-value">{result.text_similarity:.1f}%</div><div class="metric-note">TF-IDF term overlap</div></div>', unsafe_allow_html=True)
    with m2:
        coverage_label = f"{result.skill_coverage:.1f}%" if result.job_skills else "N/A"
        st.markdown(f'<div class="metric-card"><div class="metric-label">Skill coverage</div><div class="metric-value">{coverage_label}</div><div class="metric-note">Detected job skills found in resume</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Skills detected</div><div class="metric-value">{len(result.resume_skills)}</div><div class="metric-note">From the built-in vocabulary</div></div>', unsafe_allow_html=True)

    good_col, gap_col = st.columns(2, gap="large")
    with good_col:
        with st.container(border=True):
            st.markdown("#### ✓ Skills found in both")
            st.caption("Skills detected in the job description and your resume.")
            st.markdown(skill_pills(result.matched_skills, "good", "No skills from the built-in list matched. Try reviewing the wording in both texts."), unsafe_allow_html=True)
    with gap_col:
        with st.container(border=True):
            st.markdown("#### ↗ Skills not detected")
            st.caption("These appeared in the job description but were not found in your resume text.")
            st.markdown(skill_pills(result.missing_skills, "missing", "No missing skills detected from the built-in list."), unsafe_allow_html=True)
            if result.missing_skills:
                st.caption("Only add a skill to your resume if it genuinely reflects your knowledge or experience.")

    with st.expander("Explore all detected skills and scoring details"):
        detected_a, detected_b = st.columns(2)
        with detected_a:
            st.markdown("**Detected in resume**")
            st.write(", ".join(result.resume_skills) or "None detected")
        with detected_b:
            st.markdown("**Detected in job description**")
            st.write(", ".join(result.job_skills) or "None detected")
        st.markdown("**Scoring method**  \n60% × TF-IDF text similarity + 40% × detected skill coverage. If no supported skills are detected in the job description, the score falls back to text similarity.")
        st.warning("The skill vocabulary is curated and incomplete. Similarity is based on shared terms, not deep semantic understanding. A missing skill means it was not detected in the text — it does not prove that you lack it.")

st.divider()
st.markdown('<div class="privacy-note">TalentLens is an educational portfolio project. It does not make hiring decisions, rank candidates or intentionally store resume text. For public deployments, review hosting-provider logs and retention settings before using real personal data.</div>', unsafe_allow_html=True)
