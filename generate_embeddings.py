#!/usr/bin/env python3
"""
Script to generate embeddings for the decision corpus.
This creates the decisions_embeddings.npy file from decisions.csv.
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

def generate_embeddings():
    """Generate embeddings for all decisions in the CSV file."""

    # Load the decisions CSV
    df = pd.read_csv('decisions.csv')

    # Combine relevant columns to create embedding text
    # We'll embed the request + proposal + outcome for similarity search
    embedding_texts = []
    for _, row in df.iterrows():
        text = f"Request: {row['request']}\nProposal: {row['proposal']}\nOutcome: {row['outcome']}"
        embedding_texts.append(text)

    # Load a pre-trained sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings
    embeddings = model.encode(embedding_texts, show_progress_bar=True)

    # Save embeddings as numpy array
    np.save('decisions_embeddings.npy', embeddings)

    print(f"Generated embeddings for {len(embedding_texts)} decisions")
    print(f"Embeddings shape: {embeddings.shape}")
    print("Saved to decisions_embeddings.npy")

if __name__ == "__main__":
    generate_embeddings()