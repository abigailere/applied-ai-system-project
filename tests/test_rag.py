import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rag_retriever import song_to_text_description, build_chromadb_index, query_chromadb

LOFI_SONG = {
    "id": 1,
    "title": "Focus Flow",
    "artist": "LoRoom",
    "genre": "lofi",
    "mood": "focused",
    "energy": 0.40,
    "tempo_bpm": 80,
    "valence": 0.59,
    "danceability": 0.60,
    "acousticness": 0.78,
}

METAL_SONG = {
    "id": 2,
    "title": "Iron Gates",
    "artist": "Voltline",
    "genre": "metal",
    "mood": "intense",
    "energy": 0.97,
    "tempo_bpm": 168,
    "valence": 0.35,
    "danceability": 0.52,
    "acousticness": 0.08,
}

AMBIENT_SONG = {
    "id": 3,
    "title": "Still Waters",
    "artist": "Orbit Bloom",
    "genre": "ambient",
    "mood": "focused",
    "energy": 0.18,
    "tempo_bpm": 55,
    "valence": 0.54,
    "danceability": 0.20,
    "acousticness": 0.95,
}

SAMPLE_SONGS = [LOFI_SONG, METAL_SONG, AMBIENT_SONG]


# --- song_to_text_description ---

def test_description_returns_string():
    result = song_to_text_description(LOFI_SONG)
    assert isinstance(result, str)

def test_description_contains_title():
    result = song_to_text_description(LOFI_SONG)
    assert LOFI_SONG["title"] in result

def test_description_contains_artist():
    result = song_to_text_description(LOFI_SONG)
    assert LOFI_SONG["artist"] in result

def test_description_contains_genre():
    result = song_to_text_description(LOFI_SONG)
    assert LOFI_SONG["genre"] in result

def test_description_contains_mood():
    result = song_to_text_description(LOFI_SONG)
    assert LOFI_SONG["mood"] in result

def test_description_contains_tempo():
    result = song_to_text_description(LOFI_SONG)
    assert str(int(LOFI_SONG["tempo_bpm"])) in result


# --- build_chromadb_index ---

def test_index_returns_collection():
    collection = build_chromadb_index(SAMPLE_SONGS)
    assert collection is not None

def test_index_contains_all_songs():
    collection = build_chromadb_index(SAMPLE_SONGS)
    assert collection.count() == len(SAMPLE_SONGS)


# --- query_chromadb ---

def test_query_returns_list():
    collection = build_chromadb_index(SAMPLE_SONGS)
    songs_by_id = {song["id"]: song for song in SAMPLE_SONGS}
    results = query_chromadb("calm music for studying", songs_by_id, collection, k=2)
    assert isinstance(results, list)

def test_query_respects_k():
    collection = build_chromadb_index(SAMPLE_SONGS)
    songs_by_id = {song["id"]: song for song in SAMPLE_SONGS}
    results = query_chromadb("late night focus session", songs_by_id, collection, k=2)
    assert len(results) <= 2

def test_query_results_have_expected_fields():
    collection = build_chromadb_index(SAMPLE_SONGS)
    songs_by_id = {song["id"]: song for song in SAMPLE_SONGS}
    results = query_chromadb("calm background music", songs_by_id, collection, k=1)
    assert "title" in results[0]
    assert "artist" in results[0]

def test_query_semantic_match():
    collection = build_chromadb_index(SAMPLE_SONGS)
    songs_by_id = {song["id"]: song for song in SAMPLE_SONGS}
    results = query_chromadb("calm music for studying late at night", songs_by_id, collection, k=1)
    assert results[0]["title"] != METAL_SONG["title"]
