"""Backend: Document Refinement — AI-powered document improvement.

Uses Gemma 4 thinking mode to improve document quality.
Supports summary, formalization, and custom refinements.

Wing: smartdoc_backend
Topic: document_refinement
Last Updated: 2026-05-05 10:15
"""

from typing import Dict, Any, Optional
from ollama_client import OllamaClient


class DocumentRefiner:
    """Refines documents using AI with thinking mode."""

    def __init__(self, ollama_client: OllamaClient):
        """Initialize document refiner.

        Args:
            ollama_client: Configured Ollama client with Gemma 4
        """
        self.ollama = ollama_client

    def summarize(self, markdown: str) -> str:
        """Generate summary of document.

        Args:
            markdown: Document text

        Returns:
            Summary text
        """
        prompt = f"""Summarize the following document:

{markdown[:5000]}

Provide a clear, concise summary that captures the main points."""

        try:
            response = self.ollama.chat(prompt=prompt, task='summary')

            if 'message' in response:
                return response['message'].get('content', 'Summary generation failed.')

        except Exception as e:
            print(f"Summary error: {e}")

        return "Could not generate summary."

    def formalize(self, markdown: str) -> str:
        """Rewrite document in formal tone.

        Args:
            markdown: Document text

        Returns:
            Formalized document
        """
        prompt = f"""Rewrite the following document in a formal, professional tone suitable for business communications:

{markdown}

Maintain the original meaning and key information, but improve clarity, structure, and professionalism."""

        try:
            response = self.ollama.chat(prompt=prompt, task='formalization')

            if 'message' in response:
                content = response['message'].get('content', 'Formalization failed.')
                return content

        except Exception as e:
            print(f"Formalization error: {e}")

        return "Could not formalize document."

    def custom_refinement(self, markdown: str, instruction: str) -> str:
        """Apply custom refinement based on user instruction.

        Args:
            markdown: Document text
            instruction: User's refinement request

        Returns:
            Refined document
        """
        prompt = f"""Refine the document according to the following instruction:

Instruction: {instruction}

Document:
{markdown}

Provide the refined document that addresses the instruction."""

        try:
            response = self.ollama.chat(prompt=prompt, task='document_refinement')

            if 'message' in response:
                content = response['message'].get('content', 'Refinement failed.')
                return content

        except Exception as e:
            print(f"Custom refinement error: {e}")

        return "Could not refine document."

    def extract_tables(self, markdown: str) -> str:
        """Extract and format tables from document.

        Args:
            markdown: Document text

        Returns:
            Formatted tables
        """
        prompt = f"""Extract all tables from the following document and format them clearly:

{markdown}

Provide the extracted tables in a clear, organized format."""

        try:
            response = self.ollama.chat(prompt=prompt, task='document_refinement')

            if 'message' in response:
                content = response['message'].get('content', 'Table extraction failed.')
                return content

        except Exception as e:
            print(f"Table extraction error: {e}")

        return "Could not extract tables."

    def improve_structure(self, markdown: str) -> str:
        """Improve document structure and formatting.

        Args:
            markdown: Document text

        Returns:
            Structurally improved document
        """
        prompt = f"""Improve the structure and formatting of the following document:

{markdown}

Organize content with clear headings, bullet points, and proper formatting while maintaining all original information."""

        try:
            response = self.ollama.chat(prompt=prompt, task='document_refinement')

            if 'message' in response:
                content = response['message'].get('content', 'Structure improvement failed.')
                return content

        except Exception as e:
            print(f"Structure improvement error: {e}")

        return "Could not improve document structure."
