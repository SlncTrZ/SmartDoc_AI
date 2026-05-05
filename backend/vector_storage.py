"""Backend: Vector Storage — Manages LanceDB for document storage.

Creates LanceDB tables, stores embeddings, provides semantic search.
Organizes documents by Wings (categories) as separate tables.

Wing: smartdoc_backend
Topic: vector_database
Last Updated: 2026-05-05 09:05
"""

import os
from typing import List, Dict, Any, Optional
import lancedb
from lancedb.pydantic import LanceModel, Vector
import pyarrow as pa
import numpy as np


# Dynamic schema - dimension will be set at runtime
def create_document_schema(dimension: int = 768):
    """Create DocumentSchema with specified embedding dimension.

    Args:
        dimension: Embedding vector dimension (768 for nomic-embed-text)

    Returns:
        LanceModel subclass for documents
    """
    class DocumentSchema(LanceModel):
        """Schema for stored documents in LanceDB."""
        id: str
        filename: str
        markdown: str
        metadata: str  # JSON string instead of Dict
        embedding: Vector(dimension)
        wing: str
        created_at: str

    return DocumentSchema


class VectorStorage:
    """Manages LanceDB operations for SmartDoc AI."""

    def __init__(self, db_path: str = "./data/lancedb", embedding_dim: int = 768):
        """Initialize LanceDB connection.

        Args:
            db_path: Path to store LanceDB database
            embedding_dim: Embedding vector dimension (768 for nomic-embed-text)
        """
        self.db_path = db_path
        self.embedding_dim = embedding_dim
        self.DocumentSchema = create_document_schema(embedding_dim)

        os.makedirs(db_path, exist_ok=True)
        self.db = lancedb.connect(db_path)

        # Default wings (categories)
        self.default_wings = [
            'tai_lieu_cong_van',
            'tai_lieu_ke_toan',
            'tai_lieu_nhan_su',
            'tai_lieu_hop_dong',
            'tai_lieu_khac'
        ]

    def create_wing(self, wing_name: str):
        """Create a new wing (table) in database.

        Args:
            wing_name: Name of the wing/table
        """
        if wing_name not in self.db.table_names():
            self.db.create_table(wing_name, schema=self.DocumentSchema)

    def ensure_wings(self, wings: Optional[List[str]] = None):
        """Ensure all required wings exist in database.

        Args:
            wings: List of wing names, uses defaults if None
        """
        wing_list = wings or self.default_wings
        for wing in wing_list:
            self.create_wing(wing)

    def add_document(self, wing: str, doc_data: Dict[str, Any]):
        """Add document to specific wing.

        Args:
            wing: Wing name
            doc_data: Document data with embedding
        """
        table = self.db.open_table(wing)
        table.add([doc_data])

    def search(self, wing: str, query_embedding: np.ndarray, limit: int = 5) -> List[Dict]:
        """Semantic search in specific wing.

        Args:
            wing: Wing name
            query_embedding: Query vector (numpy array)
            limit: Number of results

        Returns:
            List of matching documents
        """
        try:
            table = self.db.open_table(wing)

            # Search using LanceDB
            results = table.search(query_embedding.tolist()).limit(limit).to_list()

            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def list_wings(self) -> List[str]:
        """Get list of all wings (tables).

        Returns:
            List of wing names
        """
        return self.db.table_names()

    def get_document_count(self, wing: str) -> int:
        """Get number of documents in wing.

        Args:
            wing: Wing name

        Returns:
            Document count
        """
        table = self.db.open_table(wing)
        return len(table)
