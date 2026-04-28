import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import patch, MagicMock
from src.explainer import generate_explanation

SAMPLE_SONG = {
    "title": "Storm Runner",
    "artist": "Voltline",
    "genre": "rock",
    "mood": "intense",
    "energy": 0.91,
    "tempo_bpm": 152
}
SAMPLE_BLURB = "Voltline is a high-octane rock act known for driving riffs and relentless energy."
SAMPLE_QUERY = "upbeat music for the gym"


def make_mock_model(response_text="Great match sentence one. Great match sentence two."):
    mock_response = MagicMock()
    mock_response.text = response_text
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    return mock_model


# --- generate_explanation ---

def test_returns_string():
    with patch("src.explainer.genai.GenerativeModel", return_value=make_mock_model()):
        result = generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        assert isinstance(result, str)

def test_returns_api_text():
    expected = "Storm Runner's relentless tempo makes it ideal. Voltline's energy matches your gym vibe."
    with patch("src.explainer.genai.GenerativeModel", return_value=make_mock_model(expected)):
        result = generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        assert result == expected

def test_fallback_on_exception():
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API error")
    with patch("src.explainer.genai.GenerativeModel", return_value=mock_model):
        result = generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        assert "Storm Runner" in result
        assert "Voltline" in result

def test_fallback_contains_mood_and_genre():
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API error")
    with patch("src.explainer.genai.GenerativeModel", return_value=mock_model):
        result = generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        assert "intense" in result
        assert "rock" in result

def test_prompt_contains_user_query():
    mock_model = make_mock_model()
    with patch("src.explainer.genai.GenerativeModel", return_value=mock_model):
        generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        call_args = mock_model.generate_content.call_args[0][0]
        assert SAMPLE_QUERY in call_args

def test_prompt_contains_song_title():
    mock_model = make_mock_model()
    with patch("src.explainer.genai.GenerativeModel", return_value=mock_model):
        generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        call_args = mock_model.generate_content.call_args[0][0]
        assert "Storm Runner" in call_args

def test_prompt_contains_artist_blurb():
    mock_model = make_mock_model()
    with patch("src.explainer.genai.GenerativeModel", return_value=mock_model):
        generate_explanation(SAMPLE_SONG, SAMPLE_BLURB, SAMPLE_QUERY)
        call_args = mock_model.generate_content.call_args[0][0]
        assert SAMPLE_BLURB in call_args
