import chromadb
from chromadb.utils import embedding_functions

#function that converts each song into a text discription
def song_to_text_description(song):
    energy = song['energy']
    if energy < 0.35:
        energy_label = "low energy"
    elif energy < 0.65:
        energy_label = "mid energy"
    else:
        energy_label = "high energy"

    danceability = song['danceability']
    if danceability < 0.35:
        dance_label = "not very danceable"
    elif danceability < 0.55:
        dance_label = "moderately danceable"
    elif danceability < 0.75:
        dance_label = "danceable"
    else:
        dance_label = "highly danceable"

    valence = song['valence']
    if valence < 0.40:
        valence_label = "dark or melancholic"
    elif valence < 0.65:
        valence_label = "neutral"
    else:
        valence_label = "uplifting or positive"

    acousticness = song['acousticness']
    if acousticness < 0.25:
        acoustic_label = "electronic or heavily produced"
    elif acousticness < 0.60:
        acoustic_label = "a mix of acoustic and electronic"
    else:
        acoustic_label = "acoustic or organic"

    plain_text = (
        f"{song['title']} by {song['artist']}. "
        f"It has a {song['mood']} mood and is {energy_label}. "
        f"It falls within the {song['genre']} genre and has a tempo of {song['tempo_bpm']} BPM. "
        f"It is {dance_label}, with a {valence_label} tone, and has an {acoustic_label} sound."
    )
    return plain_text
 
#function that builds ChromaDB song index at startup
def build_chromadb_index(songs):
    doc_list = []
    for song in songs:
        doc_list.append(song_to_text_description(song))
    ids = [str(song["id"]) for song in songs]
    client = chromadb.EphemeralClient()
    ef = embedding_functions.DefaultEmbeddingFunction()
    try:
        client.delete_collection("songs")
    except Exception:
        pass
    song_collection = client.create_collection(name="songs", embedding_function=ef)  # type: ignore
    song_collection.add(documents=doc_list, ids=ids)
    return song_collection

#function that takes user's natural language query and returns top 5 matching songs
def query_chromadb(user_query, songs_by_id, collection, k=5):
    results = collection.query(query_texts=[user_query], n_results=k)
    retrieved_songs = []
    for id in results["ids"][0]:
        song = songs_by_id[int(id)]
        retrieved_songs.append(song)
    return retrieved_songs


if __name__ == "__main__":
    import os
    from recommender import load_songs

    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(csv_path)
    songs_by_id = {song["id"]: song for song in songs}

    print("Building index...")
    collection = build_chromadb_index(songs)
    print(f"Index ready — {collection.count()} songs loaded.\n")

    while True:
        query = input("Enter a query (or 'quit' to exit): ").strip()
        if query.lower() == "quit":
            break
        results = query_chromadb(query, songs_by_id, collection, k=5)
        print()
        for i, song in enumerate(results, 1):
            print(f"  #{i}  {song['title']}  —  {song['artist']}  ({song['genre']}, {song['mood']})")
        print()
  