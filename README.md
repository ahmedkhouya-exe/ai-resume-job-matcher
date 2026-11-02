# TalentLens — AI Resume & Job Matcher

A dark, green-accented Streamlit career dashboard for comparing resume text with job descriptions.

## Front-end view

### Dashboard and match results
![TalentLens dashboard and match report](front-end%20view/dashboard.png)

### Resume upload and job description
![Resume upload and target job input form](front-end%20view/resume-inputs.png)

## Features
- Dark dashboard with responsive styling and high-contrast inputs
- Upload TXT, PDF, or DOCX resumes or paste resume text
- Match score, text similarity, skill coverage, matched and missing keywords
- Sample data, recommendations, unit tests, and GitHub Actions

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```
Open the URL printed by Streamlit, usually http://localhost:8501.

## Scoring
The score combines TF-IDF cosine similarity (55%) with curated skill coverage (45%). This is a transparent baseline, not a hiring prediction or a full semantic AI model.
