"""Backend: RAG Pipeline — Retrieval-Augmented Generation.

Combines semantic search with AI generation.
Supports dual providers: Ollama (local) + ds2api (DeepSeek web).

Wing: smartdoc_backend
Topic: rag_implementation
Updated: 2026-05-06
"""

from typing import List, Dict, Any, Optional
from embedding_service import EmbeddingService
from vector_storage import VectorStorage
from ollama_client import OllamaClient
from ds2api_client import DS2APIClient


class RAGPipeline:
    """RAG pipeline for document-based Q&A."""

    def __init__(self,
                 embedding_service: EmbeddingService,
                 storage: VectorStorage,
                 ollama_client: OllamaClient,
                 ds2api_client: Optional[DS2APIClient] = None):
        """Initialize RAG pipeline.

        Args:
            embedding_service: Embedding generation service
            storage: Vector database
            ollama_client: AI client (local Ollama)
            ds2api_client: Optional ds2api client (cloud DeepSeek)
        """
        self.embedding_service = embedding_service
        self.storage = storage
        self.ollama_client = ollama_client
        self.ds2api_client = ds2api_client or DS2APIClient()
        self.provider = "ollama"  # default

    def retrieve(self, query: str, wings: Optional[List[str]] = None, limit: int = 5) -> List[Dict]:
        """Retrieve relevant documents for a query.

        Args:
            query: User query
            wings: List of wings to search (default: all)
            limit: Number of results

        Returns:
            List of relevant documents
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)

        # Get wings to search
        search_wings = wings or self.storage.list_wings()

        # Search all wings
        all_results = []
        for wing in search_wings:
            results = self.storage.search(wing, query_embedding, limit)
            all_results.extend(results)

        # Sort by score and limit results
        all_results.sort(key=lambda x: x.get('_score', 0), reverse=True)
        return all_results[:limit]

    def generate(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response using retrieved context.

        Args:
            query: User query
            context_docs: Retrieved documents

        Returns:
            Generated response
        """
        # Build context from retrieved documents
        context_parts = []
        for doc in context_docs:
            try:
                import json
                metadata = json.loads(doc.get('metadata', '{}'))
                context_parts.append(f"Document: {doc.get('filename', 'Unknown')}")
                context_parts.append(f"Content: {doc.get('markdown', '')[:500]}...")
                context_parts.append("---")
            except:
                continue

        context = "\n\n".join(context_parts)

        # Build prompt
        prompt = f"""You are an AI assistant helping users find information in documents.

Question: {query}

Reference documents:
{context}

Answer the question based on the information in the documents. If information is not found, state clearly.
Answer in Vietnamese, keep it concise and easy to understand."""

        # Generate response (try ds2api first if available, fallback to Ollama)
        if self.provider == "ds2api" and self.ds2api_client and self.ds2api_client.is_available():
            try:
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Answer based on the reference documents."},
                    {"role": "user", "content": prompt}
                ]
                result = self.ds2api_client.chat(messages)
                if result:
                    return result
            except Exception as e:
                print(f"[RAG] ds2api error, falling back to Ollama: {e}")

        try:
            response = self.ollama_client.chat(prompt=prompt)

            if 'message' in response:
                return response['message'].get('content', 'Sorry, an error occurred.')
            else:
                return "Sorry, could not generate response."
        except Exception as e:
            print(f"Generation error: {e}")
            return "Sorry, could not generate response."

    def query(self, query: str, wings: Optional[List[str]] = None, limit: int = 5) -> Dict[str, Any]:
        """Full RAG query: retrieve and generate.

        Args:
            query: User query
            wings: Wings to search
            limit: Number of documents to retrieve

        Returns:
            Dictionary with response and sources
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(query, wings, limit)

        # Generate response
        response_text = self.generate(query, retrieved_docs)

        # Format sources
        sources = []
        seen_files = set()
        for doc in retrieved_docs:
            filename = doc.get('filename', 'Unknown')
            if filename not in seen_files:
                sources.append({
                    'filename': filename,
                    'wing': doc.get('wing', ''),
                    'score': doc.get('_score', 0)
                })
                seen_files.add(filename)

        return {
            'response': response_text,
            'sources': sources,
            'num_documents': len(retrieved_docs)
        }

    def embed_document(self, markdown: str) -> List[Dict]:
        """Embed document into chunks with vectors.

        Args:
            markdown: Document text in markdown

        Returns:
            List of chunk data with embeddings
        """
        # Split into chunks
        chunks = self.embedding_service.chunk_text(markdown)

        # Generate embeddings for each chunk
        embeddings = self.embedding_service.generate_embeddings_batch(chunks)

        # Create chunk data
        chunk_data = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_data.append({
                'index': i,
                'text': chunk,
                'embedding': embedding.tolist(),
                'length': len(chunk)
            })

        return chunk_data
