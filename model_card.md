# 🎧 Model Card: Press 'Enter' to Resonate

---

## Architectural Overview
The system follows a Retrieval-Augmented Generation (RAG) pipeline with five stages:

**1. Startup (Index Building)**
At launch, the app reads `songs.csv` and `artist_facts.csv`. Each song is converted into a plain-English description and these descriptions along with the artist blurbs are stored in two ChromaDB collections: one for songs (~50 vectors) and one for artists (~15 vectors).

**2. User Input**
The user types a natural language query (e.g., "something calm for late-night studying"). That query is embedded into the same vector space using the a sentence-transformers model, producing a query vector that can be compared against stored song vectors.

**3. Retrieval (the R in RAG)**
ChromaDB performs a similarity search between the query vector and all song vectors, returning the top closest match The artist blurb is then fetched from the artist index using an exact ID lookup by artist name.

**4. Augmentation (the A in RAG)**
The matched song's metadata and its artist blurb are injected into a structured prompt alongside the original user query. This gives the language model grounded, real data to reason from rather than relying on general knowledge.

**5. Generation (the G in RAG)**
An augmented prompt is sent to the Google Gemini API, which generates a 2-sentence explanation of why that song fits the user's requested vibe and the result is presented with an AI-generated explaination for the choice.

```
## Design Decisions
- I decided to implement RAG into my project because I believe that is a natural upgrade to the music recommender I built for project 3. I wanted to keep the same mission/goal of having this system be useful for playlist creation based on a user's mood. Having semantic input, better replicates how music apps like Spotify build their own playlists and provide the most flexibility. 
- The local CSV files of song and artist lists allows for reproducibility meaning the system would return the same output for the same input, ensuring predictable behavior. It also makes it easier to edit the song catalog without touching code The tradeoff is local CSV files limit my catalog so recommendations are only as good as what's in the file. 
- I added artist blurbs to make the system feel more personalized and simulate the beginning steps of how finding music via similar artists would be used.
- songs and artists are stored in two separate ChromaDB collections because they serve different purposes: the song index is searched semantically using the user's query vector, while the artist index is looked up by exact name once a song is already matched. This means the system only uses semantic search where it adds value. 
- The five-stage RAG pipeline (Startup, Input, Retrieval, Augmentation, Generation) maps directly to the RAG pattern, making each stage easy to test or replace independently — for example, swapping Gemini for a different model only requires changing the Generation step.

## Testing Summary

- I used both unit testing and manual testing for my project. One of the biggest takeaways I got from Project 3's recommender was the importance of testing early and small so it’s easier to find potential bugs later. This took longer, but it made sure that every piece of my system was working as intended before piecing them together, whereas if something broke then, it would be easier to track where the issue was. I split up testing into separate files that corresponded to each file in my src folder and tested as soon as they were done before commiting.
- My biggest obstical was testing the entire thing because on Gemini's free tier, requests are limited. I had to be mindful of when I wanted to test manually because testing something unnecessary would waste a request. I ended up switching between several models because of this. I used mock unit testing to get around this.

## Reflection

What are the limitations or biases in your system?
- My system is dependent on the quality of my songs CSV file meaning the diversity of the output depends on the diversity of my list. The list of songs can easily skew in the direction of a specific genre or sound creating an over-representation of a type of song leading to less accurate results.

- The thing that surprised me the most was how difficult it was to make sure my data was holistic so that my AI was reliable. Because I used AI to generate songs for the CSV file, the genres of songs lacked diversity. There was a blind spot in generating songs with genres originating in Black and Latin music, something I had to go back and correct manually. Interestingly enough, this was something that was pointed out by the AI that I had missed, and yet it did not try to fix it unless it was prompted to. I believe this issue stems from the training data for Claude that may have racial biases. I think, if this project was replicated at mass scale, a blind spot like this could be exploited to make it harder for non-white and non-western artists to be discovered my music enthusiasts. One way to alleviate this would be to add a check in the prompt that ensures the song choices are balanced and more representative of the state of music today.

- When thinking of how to expand project 3, my goal was to have a more hand-on approach to development, using AI as the coach rather than the generator. I used Claude Code to help brainstorm my ideas for the project and plan the structure. For each step in my development process, I asked for general advice on what types of functions I may need and their role, specifying not providing code. Development took longer but, I feel I learned more and was introduced to new python libraries. Claude Code was helpful in generating tests for each file, as they were relevant to how the project would be used. However, besides having to manually look over its generated CSV song file, when suggesting the prompt to give to Gemini, it included variables that I did not intend to include as context, so had to remove them. I would like to create a frontend for the app rather than having it run through the CLI to make it feel more like a product for shipment. 
