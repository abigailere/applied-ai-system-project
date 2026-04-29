import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import patch, MagicMock
from src.rag_retriever import build_chromadb_index, query_chromadb
from src.context_retriever import load_artists_facts, build_artist_index, get_artist_context
from src.explainer import generate_explanation
from src.recommender import load_songs

SONGS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
ARTISTS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "artist_facts.csv")


def make_mock_model(response_text="Great match. Perfect for your vibe."):
    mock_response = MagicMock()
    mock_response.text = response_text
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    return mock_model


# --- data loading ---

def test_songs_csv_loads():
    songs = load_songs(SONGS_CSV)
    assert len(songs) == 54

def test_artist_csv_loads():
    artist_facts = load_artists_facts(ARTISTS_CSV)
    assert len(artist_facts) == 31

def test_songs_have_required_fields():
    songs = load_songs(SONGS_CSV)
    required = {"id", "title", "artist", "genre", "mood", "energy", "tempo_bpm"}
    for song in songs:
        assert required.issubset(song.keys())


# --- full retrieval pipeline ---

def test_pipeline_returns_five_results():
    songs = load_songs(SONGS_CSV)
    songs_by_id = {song["id"]: song for song in songs}
    collection = build_chromadb_index(songs)
    results = query_chromadb("upbeat songs for the gym", songs_by_id, collection, k=5)
    assert len(results) == 5

def test_pipeline_results_are_song_dicts():
    songs = load_songs(SONGS_CSV)
    songs_by_id = {song["id"]: song for song in songs}
    collection = build_chromadb_index(songs)
    results = query_chromadb("chill music for studying", songs_by_id, collection, k=3)
    for result in results:
        assert "title" in result
        assert "artist" in result
        assert "mood" in result

def test_artist_context_found_for_retrieved_songs():
    songs = load_songs(SONGS_CSV)
    songs_by_id = {song["id"]: song for song in songs}
    song_collection = build_chromadb_index(songs)
    artist_facts = load_artists_facts(ARTISTS_CSV)
    artist_collection = build_artist_index(artist_facts)

    results = query_chromadb("happy upbeat pop", songs_by_id, song_collection, k=5)
    for song in results:
        blurb = get_artist_context(song["artist"], artist_collection)
        assert isinstance(blurb, str)
        assert len(blurb) > 0


# --- full end-to-end with mocked Gemini ---

def test_full_pipeline_produces_explanations():
    songs = load_songs(SONGS_CSV)
    songs_by_id = {song["id"]: song for song in songs}
    song_collection = build_chromadb_index(songs)
    artist_facts = load_artists_facts(ARTISTS_CSV)
    artist_collection = build_artist_index(artist_facts)

    results = query_chromadb("something moody and atmospheric", songs_by_id, song_collection, k=5)

    with patch("src.explainer.genai.GenerativeModel", return_value=make_mock_model()):
        for song in results:
            blurb = get_artist_context(song["artist"], artist_collection)
            explanation = generate_explanation(song, blurb, "something moody and atmospheric")
            assert isinstance(explanation, str)
            assert len(explanation) > 0
