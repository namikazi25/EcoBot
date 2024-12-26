import pandas as pd
import open_clip
import torch
import chromadb
from chromadb.config import Settings

# Paths
subset_path = "./Database/subset_test.csv"

# Load the subset
df = pd.read_csv(subset_path)

# Load the BioTrove-CLIP model
model, _, _ = open_clip.create_model_and_transforms("hf-hub:BGLab/BioTrove-CLIP")
tokenizer = open_clip.get_tokenizer("hf-hub:BGLab/BioTrove-CLIP")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chromadb_test")

# Create or get the collection
collection_name = "biodiversity_test"
collection = client.get_or_create_collection(name=collection_name)

# Process and store embeddings
for idx, row in df.iterrows():
    # Combine metadata fields into a single text description
    combined_text = f"Scientific Name: {row['scientificName']}, Taxon Rank: {row['taxonRank']}, Photo URL: {row['photo_url']}"

    # Tokenize and generate embedding
    tokenized = tokenizer(combined_text).to(device)
    with torch.no_grad():
        embedding = model.encode_text(tokenized).cpu().numpy().tolist()

    print(f"Generated embedding for ID {row['photo_id']}.
    
          
          ")

    # Add embedding to the collection
    collection.add(
        ids=[str(row["photo_id"])],  # Use photo_id as unique ID
        embeddings=embedding,
        metadatas=[{
            "scientificName": row["scientificName"],
            "taxonRank": row["taxonRank"],
            "photo_url": row["photo_url"]
        }]
    )
    print(f"Stored embedding for ID {row['photo_id']} in ChromaDB.")
# Print success message
print("Embeddings stored successfully in ChromaDB!")
