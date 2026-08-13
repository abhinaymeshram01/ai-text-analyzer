import json

import pytest

from app.analyzer import summarize_text


FAKE_GEMINI_RESPONSE = {
    "summary": "The company plans to launch a new product in September.",
    "key_points": [
        "Product launch planned for September.",
        "Marketing campaign due August 20."
    ],
    "keywords": [
        "product launch",
        "marketing campaign"
    ],
    "sentiment": "Neutral",
    "entities": [
        "August 20"
    ],
    "action_items": [
        "Prepare the marketing campaign by August 20."
    ]
}


def fake_generate_response(prompt):
    """Fake Gemini response for testing."""

    return json.dumps(FAKE_GEMINI_RESPONSE)


@pytest.fixture
def mock_gemini(monkeypatch):

    monkeypatch.setattr(
        "app.analyzer.generate_response",
        fake_generate_response
    )


def test_empty_text():

    with pytest.raises(ValueError, match="Text cannot be empty."):

        summarize_text(
            "",
            "short"
        )


def test_result_structure(mock_gemini):

    text = """
    Our company will launch a new product in September.
    The marketing team will prepare the campaign by August 20.
    """

    result = summarize_text(
        text,
        "short"
    )

    if isinstance(result, str):

        result = json.loads(result)

    assert isinstance(result, dict)

    assert "summary" in result
    assert "key_points" in result
    assert "keywords" in result
    assert "sentiment" in result
    assert "entities" in result
    assert "action_items" in result


def test_long_text(mock_gemini):

    long_text = (
        "This is a test sentence about a company "
        "launching a new product. "
    ) * 1000

    result = summarize_text(
        long_text,
        "short"
    )

    if isinstance(result, str):

        result = json.loads(result)

    assert isinstance(result, dict)

    assert "summary" in result
    assert "key_points" in result
    assert "keywords" in result
    assert "sentiment" in result
    assert "entities" in result
    assert "action_items" in result