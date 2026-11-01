from matcher import match_resume_to_job, extract_text

def test_matcher_returns_expected_fields():
    result = match_resume_to_job("Python SQL Git data analysis", "Python SQL Git and data analysis")
    assert 0 <= result["match_score"] <= 100
    assert {"similarity", "skill_coverage", "matched_skills", "missing_skills", "suggestions"} <= result.keys()

def test_missing_skills_are_detected():
    result = match_resume_to_job("Python and SQL", "Python SQL Docker and AWS")
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]
    assert "aws" in result["missing_skills"]

def test_txt_extraction():
    assert extract_text("resume.txt", b"Hello resume") == "Hello resume"
