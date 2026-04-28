"""
Function that takes a song + artist blurb + user query and sends them to Google Gemini
Returns a 2-sentence natural language explanation
use python-dotenv to load the API key, instantiate the Anthropic client, and call claude-haiku-4-5-20251001
The system prompt should frame Google Gemini as a music curator. Wrap the call in a try/except so if the API fails, it returns a fallback string built from the song metadata.
"""

from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

def generate_explanation(song, artist_blurb, user_query):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="You are a music curator who crafts personalized explanations for why a song matches a listener's vibe."
    )
    ggemini_prompt = f"""You are a music curator who crafts personalized explanations for why a song matches a listener's vibe. Here is the information you have to work with: {song['title']} by {song['artist']}, which has a {song['mood']} mood, falls within the {song['genre']} genre, and has a tempo of {song['tempo_bpm']} BPM. The artist is described as: {artist_blurb}. The listener said they were in the mood for: "{user_query}". Based on this information, write a concise 2-sentence explanation of why this song is a great match for the listener's vibe. Focus on the most compelling connections between the song's characteristics, the artist's style, and the listener's expressed preferences."""
    try:
        response = model.generate_content(ggemini_prompt)
        return response.text
    except Exception as e:
        print(f"API call failed: {e}")
        return f"{song['title']} by {song['artist']} - a {song['mood']} {song['genre']} track that may match your query."

if __name__ == "__main__":
    sample_query = "upbeat music for the gym"
    sample_song = {
        "title": "Storm Runner",
        "artist": "Voltline",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.91,
        "tempo_bpm": 152
    }
    sample_blurb = "Voltline is a high-octane rock act known for driving riffs and relentless energy. Their sound is built for peak moments and pushing limits."

    explanation = generate_explanation(sample_song, sample_blurb, sample_query)
    print(f"\nSong: {sample_song['title']} by {sample_song['artist']}")
    print(f"Query: {sample_query}")
    print(f"\nExplanation:\n{explanation}")
    