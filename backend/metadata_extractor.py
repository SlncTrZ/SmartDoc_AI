"""Backend: Metadata Extractor — Extracts document metadata using AI.

Uses Ollama to analyze documents and extract structured metadata.
Processes titles, authors, dates, and document types.

Wing: smartdoc_backend
Topic: metadata_extraction
Last Updated: 2026-05-05 09:05
"""

from typing import Dict, Any, Optional
from ollama_client import OllamaClient


class MetadataExtractor:
    """Extracts metadata from documents using AI."""

    def __init__(self, ollama_client: OllamaClient):
        """Initialize metadata extractor.

        Args:
            ollama_client: Configured Ollama client
        """
        self.ollama = ollama_client

    def extract_metadata(self, markdown_content: str, filename: str, images: Optional[List[str]] = None) -> Dict[str, Any]:
        """Extract structured metadata from document using Gemma 4.

        Args:
            markdown_content: Document text in markdown
            filename: Source filename
            images: Optional list of PDF page images for multimodal analysis

        Returns:
            Dictionary with extracted metadata
        """
        # Build prompt for metadata extraction
        prompt = f"""Extract metadata from document: {filename}

Extract the following information in JSON format:
- title: Main document title
- date: Date (if available)
- author: Author or department (if available)
- document_type: Type (cong_van, hop_dong, bao_cao, khac)
- summary: Brief summary (1-2 sentences)

Document content:
{markdown_content[:3000]}

Return JSON only:
{{
  "title": "...",
  "date": "...",
  "author": "...",
  "document_type": "...",
  "summary": "..."
}}"""

        try:
            # Use Gemma 4 with system prompt and optional images
            response = self.ollama.chat(
                prompt=prompt,
                task='metadata_extraction',
                images=images  # Pass images for multimodal analysis
            )

            if 'message' in response:
                import json
                content = response['message']['content']

                # Try to parse JSON from response
                try:
                    # Clean markdown code blocks if present
                    content = content.replace('```json', '').replace('```', '').strip()
                    metadata = json.loads(content)
                except json.JSONDecodeError:
                    # Fallback: extract from text
                    metadata = {
                        'title': filename,
                        'date': '',
                        'author': '',
                        'document_type': 'khac',
                        'summary': ''
                    }

                return metadata

        except Exception as e:
            print(f"Metadata extraction error: {e}")

        # Fallback metadata
        return {
            'title': filename,
            'date': '',
            'author': '',
            'document_type': 'khac',
            'summary': ''
        }

    def classify_wing(self, metadata: Dict[str, Any]) -> str:
        """Classify document into appropriate wing based on metadata.

        Args:
            metadata: Extracted metadata

        Returns:
            Wing name
        """
        doc_type = metadata.get('document_type', 'khac')

        wing_mapping = {
            'cong_van': 'tai_lieu_cong_van',
            'hop_dong': 'tai_lieu_hop_dong',
            'bao_cao': 'tai_lieu_khac',
            'khac': 'tai_lieu_khac'
        }

        return wing_mapping.get(doc_type, 'tai_lieu_khac')
