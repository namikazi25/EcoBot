import open_clip
import torch
import chromadb
from chromadb.config import Settings

# Load the BioTrove-CLIP model
model, _, _ = open_clip.create_model_and_transforms("hf-hub:BGLab/BioTrove-CLIP")
tokenizer = open_clip.get_tokenizer("hf-hub:BGLab/BioTrove-CLIP")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chromadb_test")
collection = client.get_collection(name="biodiversity_test")

# Query the database
query_text = "What species have the taxon rank 'species'?"
tokenized_query = tokenizer(query_text).to(device)

# Generate query embedding
with torch.no_grad():
    query_embedding = model.encode_text(tokenized_query).cpu().numpy()[0].tolist()

# Search ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# Retrieve and display metadata
print("Query Results:")
for result_id in results["ids"][0]:
    metadata = collection.get(ids=[result_id])["metadatas"][0]
    print(f"Scientific Name: {metadata['scientificName']}")
    print(f"Taxon Rank: {metadata['taxonRank']}")
    print(f"Photo URL: {metadata['photo_url']}")
    print("-" * 30)
