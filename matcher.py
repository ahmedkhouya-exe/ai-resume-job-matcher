"""Explainable NLP matching logic for resume and job-description text."""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Iterable
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS: tuple[str, ...] = (
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "html", "css", "react", "angular", "vue", "node.js", "flask", "django", "fastapi", "streamlit", "machine learning", "deep learning", "natural language processing", "nlp", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "data analysis", "data visualization", "statistics", "power bi", "tableau", "excel", "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "linux", "bash", "ci/cd", "api", "rest api", "mongodb", "postgresql", "mysql", "mariadb", "redis", "communication", "teamwork", "problem solving", "project management", "agile", "scrum", "cybersecurity", "networking", "computer networks", "oop", "object-oriented programming", "testing", "pytest", "selenium",
)

@dataclass(frozen=True)
class MatchResult:
    match_score: int
    text_similarity: float
    skill_coverage: float
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    summary: str


def extract_skills(text: str, skills: Iterable[str] = SKILLS) -> list[str]:
    normalized = re.sub(r"\s+", " ", text or "").strip().lower()
    return [skill for skill in skills if re.search(r"(?<![\w+#.])" + re.escape(skill.lower()) + r"(?![\w+#.])", normalized)]


def calculate_text_similarity(resume_text: str, job_description: str) -> float:
    resume, job = (resume_text or "").strip(), (job_description or "").strip()
    if not resume or not job: return 0.0
    try:
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform([resume, job])
        return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0, 0]) * 100, 2)
    except ValueError: return 0.0


def analyze_match(resume_text: str, job_description: str) -> MatchResult:
    if not (resume_text or "").strip(): raise ValueError("Resume text cannot be empty.")
    if not (job_description or "").strip(): raise ValueError("Job description cannot be empty.")
    resume_skills, job_skills = extract_skills(resume_text), extract_skills(job_description)
    resume_set = set(resume_skills)
    matched = [s for s in job_skills if s in resume_set]
    missing = [s for s in job_skills if s not in resume_set]
    similarity = calculate_text_similarity(resume_text, job_description)
    if job_skills:
        coverage = round(len(matched) / len(job_skills) * 100, 2)
        overall = round(0.6 * similarity + 0.4 * coverage)
        summary = f"Your resume includes {len(matched)} of {len(job_skills)} skills detected in the job description. Review the missing-skill list and ensure your resume accurately reflects your experience."
    else:
        coverage, overall = 0.0, round(similarity)
        summary = "No skills from the built-in vocabulary were detected in the job description, so the score uses text similarity only."
    return MatchResult(max(0,min(100,int(overall))), similarity, coverage, matched, missing, resume_skills, job_skills, summary)
