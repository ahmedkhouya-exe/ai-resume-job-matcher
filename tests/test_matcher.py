import pytest
from matcher import analyze_match, calculate_text_similarity, extract_skills


def test_extracts_skills_case_insensitively():
    assert extract_skills("Experienced PYTHON developer with SQL and pandas") == ["python", "sql", "pandas"]


def test_java_does_not_match_javascript():
    assert "java" not in extract_skills("Built interfaces with JavaScript")
    assert "javascript" in extract_skills("Built interfaces with JavaScript")


def test_identical_text_has_high_similarity():
    text = "Python developer with SQL experience and data analysis skills"
    assert calculate_text_similarity(text, text) == pytest.approx(100.0)


def test_similarity_empty_text_is_zero():
    assert calculate_text_similarity("", "Python engineer") == 0.0


def test_analyze_match_finds_missing_skills():
    result = analyze_match("Python developer. Used pandas, SQL, and Git on data analysis projects.", "We need Python, SQL, Docker, AWS, and Git experience.")
    assert set(result.matched_skills) == {"python", "sql", "git"}
    assert set(result.missing_skills) == {"docker", "aws"}
    assert result.skill_coverage == 60.0
    assert 0 <= result.match_score <= 100


def test_empty_inputs_raise_clear_errors():
    with pytest.raises(ValueError, match="Resume text"): analyze_match("  ", "Python engineer")
    with pytest.raises(ValueError, match="Job description"): analyze_match("Python developer", "")


def test_job_without_supported_skills_uses_text_similarity():
    result = analyze_match("I like building useful products", "We build useful products for customers")
    assert result.skill_coverage == 0.0
    assert result.match_score == round(result.text_similarity)
    assert "text similarity only" in result.summary
