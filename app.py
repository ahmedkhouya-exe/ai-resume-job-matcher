import streamlit as st
from matcher import extract_text, match_resume_to_job

st.set_page_config(page_title="TalentLens | Career Match", page_icon="◆", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root{--bg:#07131f;--panel:#0d1b29;--line:#20384a;--text:#f4f7fb;--muted:#a8b8c8;--green:#39d98a;--amber:#f6bd60}
html,body,[data-testid="stAppViewContainer"],.stApp{background:#07131f!important;color:#f4f7fb!important}
[data-testid="stHeader"]{background:transparent!important}
.block-container{max-width:1440px;padding:2rem 3rem 4rem!important}
h1,h2,h3,h4,strong{color:#f4f7fb!important;letter-spacing:-.025em}
p,li,label,.stMarkdown,[data-testid="stCaptionContainer"]{color:#a8b8c8}
a{color:#39d98a!important}
.hero-kicker{font-size:.76rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#39d98a;margin-bottom:1.2rem}
.hero-title{font-size:clamp(2.5rem,4vw,4.5rem);line-height:1.04;font-weight:850;letter-spacing:-.055em;color:#f7fafc;margin:0 0 1.2rem}
.hero-copy{font-size:1.06rem;line-height:1.75;max-width:550px;color:#aebdca;margin-bottom:1.7rem}
.feature{display:flex;gap:14px;align-items:flex-start;margin:1.2rem 0}
.feature-icon{width:46px;height:46px;flex:0 0 46px;border-radius:12px;background:#102b2a;border:1px solid #1a4940;display:flex;align-items:center;justify-content:center;color:#39d98a;font-size:1.4rem}
.feature-title{font-weight:750;color:#f2f6f9;margin-bottom:.25rem}.feature-copy{color:#96a9b9;line-height:1.5;font-size:.93rem}
.panel{background:linear-gradient(145deg,#0d1c2a,#0b1925);border:1px solid #20384a;border-radius:22px;padding:1.5rem}
.panel-head{font-size:1.05rem;font-weight:800;color:#f6f8fa;margin-bottom:.25rem}.panel-sub{color:#91a5b7;font-size:.88rem;margin-bottom:1.2rem}
.score-circle{width:210px;height:210px;border-radius:50%;border:12px solid #203643;border-top-color:#39d98a;border-right-color:#39d98a;border-bottom-color:#39d98a;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:1.2rem auto;background:radial-gradient(circle,#102536,#0b1925 72%)}
.score-number{font-size:3rem;line-height:1;font-weight:850;color:#fff}.score-label{font-size:1rem;font-weight:700;color:#39d98a;margin-top:.5rem}
.section-label{font-size:1rem;font-weight:800;color:#f6f8fa;margin:1rem 0 .8rem}
.chip{display:inline-block;padding:.45rem .62rem;border-radius:8px;font-size:.82rem;margin:0 .3rem .4rem 0;border:1px solid}
.chip-good{color:#7aefb1;background:#0d3027;border-color:#1d5d43}.chip-missing{color:#ffd083;background:#342719;border-color:#76542a}
.mini-stat{border:1px solid #20384a;background:#0b1925;border-radius:14px;padding:.9rem 1rem}.mini-label{font-size:.75rem;color:#91a5b7;margin-bottom:.3rem}.mini-value{font-size:1.45rem;font-weight:800;color:#f5f8fa}
.stButton>button{background:linear-gradient(100deg,#16875b,#24c780)!important;color:#04150f!important;border:0!important;border-radius:12px!important;font-weight:800!important;min-height:3rem}
.stButton>button:hover{filter:brightness(1.08);box-shadow:0 0 0 2px #2fd48c33}
.stTextArea textarea,.stTextInput input,[data-testid="stFileUploaderDropzone"]{background:#0a1723!important;color:#f4f7fb!important;border:1px solid #2b4355!important;border-radius:12px!important;-webkit-text-fill-color:#f4f7fb!important;caret-color:#39d98a!important}
.stTextArea textarea::placeholder,.stTextInput input::placeholder{color:#71879a!important;-webkit-text-fill-color:#71879a!important;opacity:1!important}
[data-testid="stFileUploaderDropzone"] *{color:#d8e2eb!important}[data-testid="stFileUploaderDropzone"] button{background:#142839!important;color:#f4f7fb!important;border:1px solid #365064!important}
hr{border-color:#20384a!important}
@media(max-width:900px){.block-container{padding:1.2rem 1rem 3rem!important}.hero-title{font-size:2.7rem}.score-circle{width:175px;height:175px}.score-number{font-size:2.4rem}}
</style>
""", unsafe_allow_html=True)

def chips(items, kind):
    if not items:
        return '<span style="color:#91a5b7">Nothing detected yet.</span>'
    return "".join(f'<span class="chip {kind}">{s.title()}</span>' for s in items)

st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:2rem">
 <div style="width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#39d98a,#159d78);display:flex;align-items:center;justify-content:center;color:#062016;font-size:1.5rem;font-weight:900">◆</div>
 <div style="font-size:1.35rem;font-weight:850;color:#f5f8fa">Talent<span style="color:#39d98a">Lens</span></div>
 <div style="margin-left:auto;color:#7f95a8;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase">AI career toolkit</div>
</div>
""", unsafe_allow_html=True)

hero, dash = st.columns([.9, 1.1], gap="large")
with hero:
    st.markdown("""
    <div class="hero-kicker">Your next career move, made clearer</div>
    <div class="hero-title">See how well<br>you match.<br><span style="color:#39d98a">Land interviews.</span></div>
    <div class="hero-copy">Compare your resume with a target role. Understand your strengths, spot missing keywords, and make your next application more intentional.</div>
    <div class="feature"><div class="feature-icon">◎</div><div><div class="feature-title">Explainable match scoring</div><div class="feature-copy">See how closely your resume aligns with the job requirements.</div></div></div>
    <div class="feature"><div class="feature-icon">↗</div><div><div class="feature-title">Actionable skill insights</div><div class="feature-copy">Find relevant skills already in your resume and identify potential gaps.</div></div></div>
    <div class="feature"><div class="feature-icon">▤</div><div><div class="feature-title">Tailored to the job</div><div class="feature-copy">Improve your resume honestly with real examples and evidence.</div></div></div>
    """, unsafe_allow_html=True)
with dash:
    if "result" not in st.session_state:
        st.markdown("""
        <div class="panel"><div style="display:flex;align-items:center;gap:12px"><div style="font-size:2rem;color:#39d98a">◉</div><div><div class="panel-head">Job Match Score</div><div class="panel-sub" style="margin:0">Your target role · Resume analysis</div></div></div>
        <div class="score-circle"><div class="score-number">--%</div><div class="score-label">Ready to analyze</div></div>
        <div style="text-align:center;color:#91a5b7;font-size:.9rem;margin-bottom:1rem">Your score and keyword insights will appear here after analysis.</div><hr>
        <div class="section-label">✓ Matched keywords</div><span class="chip chip-good">Skills from both texts</span><span class="chip chip-good">Relevant experience</span>
        <div class="section-label" style="margin-top:1rem">⚠ Missing keywords</div><span class="chip chip-missing">Potential skill gaps</span><span class="chip chip-missing">Role requirements</span></div>
        """, unsafe_allow_html=True)
    else:
        r = st.session_state["result"]
        score = r["match_score"]
        label = "Strong Match" if score >= 75 else ("Good Match" if score >= 50 else "Room to Improve")
        st.markdown(f"""
        <div class="panel"><div style="display:flex;align-items:center;gap:12px"><div style="font-size:2rem;color:#39d98a">◉</div><div><div class="panel-head">Job Match Score</div><div class="panel-sub" style="margin:0">Resume · Target job</div></div></div>
        <div class="score-circle"><div class="score-number">{score}%</div><div class="score-label">{label}</div></div>
        <div style="text-align:center;color:#a8b8c8;font-size:.9rem;margin-bottom:1rem">Text-based estimate, not a hiring probability.</div>
        <div class="section-label">Matched keywords</div>{chips(r["matched_skills"],"chip-good")}
        <div class="section-label" style="margin-top:1rem">Missing keywords</div>{chips(r["missing_skills"],"chip-missing")}</div>
        """, unsafe_allow_html=True)
        q1,q2=st.columns(2)
        q1.markdown(f'<div class="mini-stat"><div class="mini-label">TEXT SIMILARITY</div><div class="mini-value">{r["similarity"]}%</div></div>',unsafe_allow_html=True)
        q2.markdown(f'<div class="mini-stat"><div class="mini-label">SKILL COVERAGE</div><div class="mini-value">{r["skill_coverage"]}%</div></div>',unsafe_allow_html=True)

st.markdown('<div style="height:1.4rem"></div><div class="panel"><div class="panel-head">Build your match report</div><div class="panel-sub">Add your resume and target job to generate a personalized comparison.</div></div>',unsafe_allow_html=True)
left,right=st.columns(2,gap="large")
with left:
    st.markdown("#### 01 · Your resume")
    st.caption("Upload a file or paste the text below.")
    upload=st.file_uploader("Resume file",type=["txt","pdf","docx"])
    default=""
    if upload:
        try: default=extract_text(upload.name,upload.getvalue())
        except Exception as exc: st.error(f"Could not read resume: {exc}")
    resume=st.text_area("Resume content",value=default,height=230,placeholder="Paste your summary, skills, work experience, education and projects…")
with right:
    st.markdown("#### 02 · Target job")
    st.caption("Paste the full job posting for a more useful comparison.")
    job=st.text_area("Job description",height=288,placeholder="Paste the role summary, responsibilities, and required skills…")
    st.caption("Tip: include required skills as well as responsibilities.")

b1,b2=st.columns([1,1.6],gap="medium")
with b1: sample=st.button("✦ Load sample data",use_container_width=True)
with b2: st.markdown('<div style="padding:.65rem 0;color:#91a5b7;font-size:.9rem">New here? Load the example resume and job description to try the app instantly.</div>',unsafe_allow_html=True)
if sample:
    st.session_state["sample_resume"]="Computer engineering student interested in data analysis and software development. Skills: Python, SQL, pandas, NumPy, Git, GitHub, Linux, HTML, CSS, JavaScript, teamwork, communication, problem solving. Built data dashboard and web application projects."
    st.session_state["sample_job"]="Junior Data Analyst. We are looking for a curious junior analyst who can use Python, SQL, pandas, NumPy and data visualization to explore datasets and communicate insights. Experience with Git, Docker, AWS and Power BI is a plus. Strong communication, teamwork and problem-solving skills are important."
    st.rerun()
if "sample_resume" in st.session_state:
    st.info("Sample data loaded. Click Analyze my match below to generate the report.")
    resume=st.session_state["sample_resume"]; job=st.session_state["sample_job"]
if st.button("✦ Analyze my match",type="primary",use_container_width=True):
    if not resume.strip() or not job.strip(): st.warning("Add both resume content and a job description first.")
    else:
        st.session_state["result"]=match_resume_to_job(resume,job)
        st.rerun()
st.markdown('<div style="color:#71879a;font-size:.8rem;text-align:center;margin-top:1.2rem">Your score is a text-based estimate, not a hiring probability or guarantee of job suitability. Resume text is analyzed during this app session.</div>',unsafe_allow_html=True)


# Day 4 upgrade: actionable recommendations and a downloadable report
if "result" in st.session_state:
    result = st.session_state["result"]
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-head">Your action plan</div><div class="panel-sub">Practical next steps based on this comparison.</div>', unsafe_allow_html=True)
    for index, suggestion in enumerate(result.get("suggestions", []), start=1):
        st.markdown(
            f'<div style="display:flex;gap:12px;align-items:flex-start;margin:.85rem 0">'
            f'<div style="flex:0 0 30px;height:30px;border-radius:9px;background:#10352b;color:#39d98a;'
            f'display:flex;align-items:center;justify-content:center;font-weight:800">{index}</div>'
            f'<div style="color:#dce6ee;line-height:1.6;padding-top:3px">{suggestion}</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    report_lines = [
        "TALENTLENS — RESUME MATCH REPORT",
        "=" * 38,
        f"Overall match score: {result['match_score']}%",
        f"Text similarity: {result['similarity']}%",
        f"Skill coverage: {result['skill_coverage']}%",
        "",
        "MATCHED SKILLS",
        *([f"- {skill.title()}" for skill in result["matched_skills"]] or ["- None detected"]),
        "",
        "SKILLS TO REVIEW",
        *([f"- {skill.title()}" for skill in result["missing_skills"]] or ["- None detected"]),
        "",
        "ACTION PLAN",
        *[f"{i}. {item}" for i, item in enumerate(result.get("suggestions", []), start=1)],
        "",
        "Note: This is a text-based estimate, not a hiring probability or guarantee of suitability.",
    ]
    st.download_button(
        "⬇ Download my match report (.txt)",
        data="\\n".join(report_lines),
        file_name="talentlens-match-report.txt",
        mime="text/plain",
        use_container_width=True,
    )
