# 🎯 AI Resume & Job Matcher

An NLP-powered Streamlit app that compares resume text with a job description, estimates text similarity, and highlights skills detected or not detected in the resume.

> **Important:** The score is a transparent heuristic for exploration, not a hiring probability or an assessment of a person's worth. The built-in skill vocabulary is curated and incomplete. A missing skill means it was not detected in the submitted text, not necessarily that the candidate lacks it.

## Features

- Paste resume text or upload a `.txt`, `.pdf`, or `.docx` resume.
- Paste a target job description.
- Calculate TF-IDF cosine similarity between the two texts.
- Detect skills from a curated, editable vocabulary.
- Display matching skills and skills not detected in the resume.
- Explain the score and show the skills detected on each side.
- Validate core behavior with pytest and GitHub Actions.

## Preview

Sample resume and job-description text are available in `examples/` for a quick local demo. Add verified application screenshots to `screenshots/` after launching the app.

## How the score works

When the job description contains skills from the built-in vocabulary:

`overall score = 0.60 × TF-IDF text similarity + 0.40 × detected skill coverage`

Skill coverage is the fraction of detected job-description skills also found in the resume. When no supported skills are detected in the job description, the overall score falls back to TF-IDF similarity. Values are rounded for display.

TF-IDF cosine similarity captures overlap in terms and phrases; it does not understand all semantic equivalents. The skill detector uses a curated phrase list, so synonyms, context, proficiency, and years of experience are not fully evaluated.

## Run locally

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Run tests

```bash
python -m pytest -q
```

Tests cover skill extraction, Java/JavaScript boundary behavior, text similarity, missing-skill analysis, invalid inputs, and fallback scoring.

## Project structure

```text
ai-resume-job-matcher/
├── .github/workflows/tests.yml
├── tests/test_matcher.py
├── examples/
│   ├── sample_resume.txt
│   └── sample_job_description.txt
├── app.py
├── matcher.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Privacy notes

This project does not implement a database or intentionally save resume content. Uploaded text is processed in the active app session. If deploying publicly, explain the deployment provider's logging and retention behavior, avoid storing submissions, and never upload another person's personal data without permission.

## Responsible use

- Use the result as a writing and skills-review aid, not an automated hiring decision.
- Never add a skill to a resume unless it truthfully reflects your experience.
- The score can be biased by wording, formatting, language, and gaps in the curated vocabulary.
- Do not use this tool to rank or reject candidates automatically.

## Roadmap

- [ ] Add anonymized example inputs and verified screenshots.
- [ ] Improve synonym handling and language support.
- [ ] Add more domain-specific skill vocabularies.
- [ ] Deploy a public demo with an explicit privacy notice.

## Tech stack

Python · Streamlit · scikit-learn · TF-IDF · cosine similarity · pytest · GitHub Actions
