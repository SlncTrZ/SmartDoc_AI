"""Backend: Document Processor — Extracts PDF/DOCX using Docling.

Handles file input, Docling API calls, markdown conversion.
Processes documents on-demand when requested by frontend.

Wing: smartdoc_backend
Topic: document_processing
Last Updated: 2026-05-05 09:05
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions


class DocumentProcessor:
    """Processes PDF and DOCX files to Markdown format."""

    def __init__(self):
        """Initialize Docling converter with optimized settings."""
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.generate_page_images = False  # Save memory

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def process_file(self, file_path: str, generate_images: bool = False) -> Dict[str, Any]:
        """Extract content from document file.

        Args:
            file_path: Path to PDF or DOCX file
            generate_images: Whether to generate page images for multimodal AI

        Returns:
            Dict with markdown content, metadata, and optional images
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            # Convert document using Docling
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.do_table_structure = True
            pipeline_options.generate_page_images = generate_images  # Generate images for Gemma 4

            converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
                }
            )

            doc = converter.convert(file_path)
            markdown_content = doc.document.export_to_markdown()

            # Extract basic metadata
            metadata = {
                'filename': Path(file_path).name,
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'page_count': len(doc.pages) if hasattr(doc, 'pages') else 0,
                'format': Path(file_path).suffix.lower().replace('.', ''),
            }

            result = {
                'markdown': markdown_content,
                'metadata': metadata,
                'success': True
            }

            # Add page images if generated
            if generate_images and hasattr(doc, 'pages'):
                try:
                    images = []
                    for page in doc.pages:
                        if hasattr(page, 'image') and page.image is not None:
                            # Convert PIL image to base64 or save to temp file
                            import base64
                            from io import BytesIO

                            buffered = BytesIO()
                            page.image.save(buffered, format="PNG")
                            img_str = base64.b64encode(buffered.getvalue()).decode()
                            images.append(img_str)

                    result['images'] = images
                    result['has_images'] = len(images) > 0

                except Exception as e:
                    print(f"Image generation error: {e}")
                    result['has_images'] = False

            return result

        except Exception as e:
            return {
                'markdown': '',
                'metadata': {'error': str(e)},
                'success': False
            }

    def batch_process(self, file_paths: list) -> list:
        """Process multiple files in batch.

        Args:
            file_paths: List of file paths

        Returns:
            List of processing results
        """
        results = []
        for file_path in file_paths:
            result = self.process_file(file_path)
            results.append(result)
        return results
