"""Backend: Embedding Service — Generates embeddings for documents.

Uses Ollama embedding model to convert text to vectors.
Stores embeddings in LanceDB for semantic search.

Wing: smartdoc_backend
Topic: embedding_generation
Last Updated: 2026-05-05 09:50
"""

import requests
import numpy as np
from typing import List, Optional
import json


class EmbeddingService:
    """Generates embeddings using Ollama."""

    def __init__(self, ollama_host: str = "http://localhost:11434", model: str = "nomic-embed-text"):
        """Initialize embedding service.

        Args:
            ollama_host: Ollama server URL
            model: Embedding model name (nomic-embed-text, mxbai-embed-large, etc.)
        """
        self.host = ollama_host
        self.embedding_model = model

        # Model dimensions mapping
        self.model_dimensions = {
            "nomic-embed-text": 768,
            "mxbai-embed-large": 1536,
            "all-minilm": 384,
        }

        # Get dimension for current model
        self.dimension = self.model_dimensions.get(model, 768)

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            Embedding vector as numpy array
        """
        try:
            payload = {
                "model": self.embedding_model,
                "prompt": text
            }

            response = requests.post(
                f"{self.host}/api/embeddings",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                embedding = data.get('embedding', [])
                return np.array(embedding, dtype=np.float32)
            else:
                print(f"Embedding error: {response.status_code}")
                return np.zeros(self.dimension, dtype=np.float32)

        except Exception as e:
            print(f"Embedding generation failed: {e}")
            return np.zeros(self.dimension, dtype=np.float32)

    def generate_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Split text into chunks for embedding.

        Args:
            text: Input text
            chunk_size: Maximum characters per chunk
            overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # Try to break at paragraph or sentence
            if end < len(text):
                # Look for paragraph break
                para_break = text.rfind('\n\n', start, end)
                if para_break > start:
                    end = para_break + 2
                else:
                    # Look for sentence break
                    sent_break = text.rfind('.', start, end)
                    if sent_break > start:
                        end = sent_break + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - overlap

        return chunks
