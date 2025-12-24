import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

# Embedding model
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Persistent ChromaDB client
client = chromadb.Client(
    Settings(
        persist_directory="../chroma_db"
    )
)

# Create or get collection
collection = client.get_or_create_collection(
    name="linkedin_styles",
    embedding_function=embedding_function
)

def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

def extract_metadata(post):
    return {
        "line_count": post.count("\n") + 1,
        "length": len(post)
    }

# Read LinkedIn posts
with open("data/linkedin_posts.txt", "r", encoding="utf-8") as f:

    posts = f.read().split("\n\n")

# Add posts to vector database
for i, post in enumerate(posts):
    post = clean_text(post)
    metadata = extract_metadata(post)

    collection.add(
        documents=[post],
        metadatas=[metadata],
        ids=[f"post_{i}"]
    )

# Persist the database

print("✅ Vector Database Created and Saved Successfully")
