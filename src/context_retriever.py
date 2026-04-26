"""
Function that builds a ChromaDB artist index from the blurbs
Function that retrieves the most relevant blurb for a given song
 you'll do exact lookup (you already know exactly which artist you want).
"""
import csv
import chromadb
from chromadb.utils import embedding_functions
def load_artists_facts(csv_path):
    # load the csv into a list of dicts
    # read the "artist" and "blurb" columns and return list of dicts
        #one per artist each with "artist" and "blurb" keys
    artist_facts = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
       # next(csv_reader, None)  # skip header row
        for row in csv_reader:
            artist_facts.append({"artist": row["artist"], "blurb": row["blurb"]})  
    return artist_facts

def build_artist_index(artist_facts):
    """
    Takes the list of artist fact dicts and builds a ChromaDB collection.

Three things to map:

    Document → the blurb text (this is what gets embedded)
    ID → the artist name string (e.g. "Neon Echo") — unlike rag_retriever.py which uses numeric IDs, 
        you use the name directly because that's what you'll look up by later
    Collection name → "artists" to keep it separate from the "songs" collection
    Everything else — creating the client, setting the embedding function, deleting an old collection before recreating — follows the exact same pattern as build_chromadb_index().
    """ 
    artist_list = [fact["artist"] for fact in artist_facts]
    blurb_list = [fact["blurb"] for fact in artist_facts]
    
    client = chromadb.EphemeralClient()
    ef = embedding_functions.DefaultEmbeddingFunction()
    try:
        client.delete_collection("artists")
    except Exception:
        pass
    name_collection = client.create_collection(name="artists", embedding_function=ef)  # type: ignore
    name_collection.add(documents=blurb_list, ids=artist_list)
    return name_collection

def get_artist_context(artist_name, collection):
    """
Takes an artist name string and the collection, returns the blurb.

Key difference from query_chromadb(): You use collection.get() instead of collection.query(). 
The distinction matters:

collection.query() does semantic search — finds the closest embedding match
collection.get() does exact ID lookup — fetches a specific record by its ID
You already know the artist name from the song dict, so semantic search would be wasteful and potentially wrong. 
You want the exact blurb for exactly that artist.
It should return the blurb string if found, or an empty string if the artist name isn't in the index — so the rest of the app doesn't break on a missing entry.
    """    
    blurb = collection.get(ids=[artist_name])  # type: ignore

    return blurb["documents"][0] if blurb["documents"] else "blurb not found"


if __name__ == "__main__":
    import os
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "artist_facts.csv")
    artist_facts = load_artists_facts(csv_path)
    collection = build_artist_index(artist_facts)
    print(f"Artist index ready — {collection.count()} artists loaded.\n")

    while True:
        name = input("Enter an artist name (or 'quit' to exit): ").strip()
        if name.lower() == "quit":
            break
        blurb = get_artist_context(name, collection)
        print(f"\n  {blurb}\n")
