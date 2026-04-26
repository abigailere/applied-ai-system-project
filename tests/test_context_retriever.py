import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.context_retriever import load_artists_facts, build_artist_index, get_artist_context

SAMPLE_FACTS = [
    {"artist": "Neon Echo", "blurb": "Neon Echo blends glossy pop melodies with retro-futuristic synth textures."},
    {"artist": "LoRoom", "blurb": "LoRoom specializes in hazy bedroom-produced lofi beats for studying."},
    {"artist": "Voltline", "blurb": "Voltline is a hard-hitting rock and metal act with relentless energy."},
]

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "artist_facts.csv")


# --- load_artists_facts ---

def test_load_returns_list():
    result = load_artists_facts(CSV_PATH)
    assert isinstance(result, list)

def test_load_returns_correct_count():
    result = load_artists_facts(CSV_PATH)
    assert len(result) == 31

def test_load_each_row_has_required_keys():
    result = load_artists_facts(CSV_PATH)
    for row in result:
        assert "artist" in row
        assert "blurb" in row

def test_load_no_empty_blurbs():
    result = load_artists_facts(CSV_PATH)
    for row in result:
        assert row["blurb"].strip() != ""


# --- build_artist_index ---

def test_index_returns_collection():
    collection = build_artist_index(SAMPLE_FACTS)
    assert collection is not None

def test_index_contains_all_artists():
    collection = build_artist_index(SAMPLE_FACTS)
    assert collection.count() == len(SAMPLE_FACTS)


# --- get_artist_context ---

def test_get_returns_string():
    collection = build_artist_index(SAMPLE_FACTS)
    result = get_artist_context("Neon Echo", collection)
    assert isinstance(result, str)

def test_get_returns_correct_blurb():
    collection = build_artist_index(SAMPLE_FACTS)
    result = get_artist_context("LoRoom", collection)
    assert result == SAMPLE_FACTS[1]["blurb"]

def test_get_returns_fallback_for_unknown_artist():
    collection = build_artist_index(SAMPLE_FACTS)
    result = get_artist_context("Unknown Artist", collection)
    assert result == "blurb not found"

def test_get_is_not_empty_for_known_artist():
    collection = build_artist_index(SAMPLE_FACTS)
    result = get_artist_context("Voltline", collection)
    assert result != "" and result != "blurb not found"
