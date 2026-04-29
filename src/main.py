from .recommender import load_songs
from .rag_retriever import build_chromadb_index, query_chromadb
from .context_retriever import load_artists_facts, build_artist_index, get_artist_context
from .explainer import generate_explanation
"""
Replace get_user_prefs() with a free-text input prompt
Replace recommend_songs() call with the ChromaDB retrieval
wire the explaination into the display for each recommended song
"""

def main() -> None:
    #load the songs
    songs = load_songs("data/songs.csv")
    song_collection = build_chromadb_index(songs)
    songs_by_id = {song["id"]: song for song in songs}
      
    #load artists
    artist_facts = load_artists_facts("data/artist_facts.csv")
    artist_collection = build_artist_index(artist_facts)
    
    #get user input
    usr_input = input("What kind of music are you in the mood for? ")

    print("\n" + "-" * 52)
    for song in query_chromadb(usr_input, songs_by_id, song_collection, k=1):
        artist_blurb = get_artist_context(song["artist"], artist_collection)
        explanation = generate_explanation(song, artist_blurb, usr_input)
        print(f"* {song['title']} by {song['artist']} * \n{explanation}\n")



if __name__ == "__main__":
    main()
