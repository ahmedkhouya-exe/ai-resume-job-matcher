from io import BytesIO
import re
from pathlib import Path

SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "mysql", "mariadb",
    "html", "css", "react", "node.js", "git", "github", "docker", "linux", "bash",
    "machine learning", "data analysis", "pandas", "numpy", "scikit-learn",
    "communication", "problem solving", "teamwork", "testing", "documentation",
    "dashboard development", "data visualization", "statistics", "excel", "power bi",
    "tableau", "api development", "cloud", "aws", "azure", "c++", "c"
]

def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        return content.decode("utf-8", errors="replace")
    if suffix == ".pdf":
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(content)).pages)
    if suffix == ".docx":
        from docx import Document
        return "\n".join(p.text for p in Document(BytesIO(content)).paragraphs)
    raise ValueError("Unsupported file type. Use TXT, PDF, or DOCX.")

def _has(text: str, skill: str) -> bool:
    pattern = r"(?<![a-z0-9+#.])" + re.escape(skill.lower()) + r"(?![a-z0-9+#.])"
    return bool(re.search(pattern, text.lower()))

def match_resume_to_job(resume: str, job: str) -> dict:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    try:
        matrix = TfidfVectorizer(stop_words="english").fit_transform([resume, job])
        similarity = round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100)
    except ValueError:
        similarity = 0
    job_skills = [s for s in SKILLS if _has(job, s)]
    matched = [s for s in job_skills if _has(resume, s)]
    missing = [s for s in job_skills if s not in matched]
    coverage = round(100 * len(matched) / len(job_skills)) if job_skills else 0
    suggestions = []
    if missing:
        suggestions.append("If you genuinely have these skills, add evidence of them: " + ", ".join(missing[:6]) + ".")
    if similarity < 35:
        suggestions.append("Use relevant terminology from the job description where it accurately reflects your experience.")
    if not matched:
        suggestions.append("Add concrete projects or work examples that demonstrate relevant skills.")
    suggestions.append("Use measurable outcomes where possible, such as time saved, users supported, or accuracy improved.")
    return {"match_score": round(.55 * similarity + .45 * coverage), "similarity": similarity,
            "skill_coverage": coverage, "matched_skills": matched, "missing_skills": missing,
            "suggestions": suggestions}
