"""Bridge Manager — Python orchestrator for all AI bridges.

" Nhạc trưởng" điều phối:
- notebooklm-mcp (Node.js + Playwright): PDF -> Markdown via Cloud
- Docling (Python): PDF -> Markdown via Local OCR (fallback)
- ds2api (Python): DeepSeek web interface

Wing: smartdoc_backend
Topic: bridge_orchestrator
Updated: 2026-05-06
"""

import os
import json
import sys
import time
import subprocess
import logging
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class BridgeManager:
    """Orchestrates document processing bridges."""

    def __init__(self, backend_dir: str = None):
        self.backend_dir = backend_dir or os.path.dirname(os.path.abspath(__file__))
        self.drivers_dir = os.path.join(self.backend_dir, "drivers")
        os.makedirs(self.drivers_dir, exist_ok=True)

        self.drivers_path = os.path.join(
            os.environ.get("APPDATA", os.path.expanduser("~")),
            "SmartDoc_AI", "drivers"
        )
        os.makedirs(self.drivers_path, exist_ok=True)

    # ──────────────────────────────────────────
    # NotebookLM Bridge
    # ──────────────────────────────────────────

    def _get_notebooklm_path(self) -> Optional[str]:
        """Find notebooklm-mcp-cli installation."""
        candidates = [
            os.path.join(self.drivers_dir, "notebooklm-mcp-cli", "index.js"),
            os.path.join(self.drivers_path, "notebooklm-mcp-cli", "index.js"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    def notebooklm_available(self) -> bool:
        """Check if notebooklm-mcp-cli is installed."""
        return self._get_notebooklm_path() is not None

    def install_notebooklm(self, progress_cb: Optional[Callable] = None) -> bool:
        """Clone and install notebooklm-mcp-cli."""
        target_dir = os.path.join(self.drivers_path, "notebooklm-mcp-cli")
        if os.path.exists(target_dir):
            return True

        try:
            if progress_cb:
                progress_cb(10, "Đang tải NotebookLM Bridge...")

            subprocess.run(
                ["git", "clone", "https://github.com/jacob-bd/notebooklm-mcp-cli.git",
                 target_dir],
                capture_output=True, timeout=60
            )

            if progress_cb:
                progress_cb(50, "Đang cài đặt dependencies...")

            subprocess.run(
                ["npm", "install"],
                cwd=target_dir,
                capture_output=True, timeout=120
            )

            if progress_cb:
                progress_cb(80, "Đang cài đặt Chromium...")

            subprocess.run(
                ["npx", "playwright", "install", "chromium"],
                cwd=target_dir,
                capture_output=True, timeout=180
            )

            if progress_cb:
                progress_cb(100, "NotebookLM Bridge sẵn sàng!")

            return True
        except Exception as e:
            logger.error(f"Failed to install notebooklm: {e}")
            return False

    def notebooklm_convert(self, pdf_path: str, timeout: int = 120) -> Optional[str]:
        """Convert PDF to Markdown via NotebookLM.

        Args:
            pdf_path: Path to PDF file
            timeout: Max wait time in seconds

        Returns:
            Markdown content or None on failure
        """
        script = self._get_notebooklm_path()
        if not script:
            logger.warning("NotebookLM not installed")
            return None

        try:
            result = subprocess.run(
                ["node", script, "convert", pdf_path, "--format", "markdown"],
                capture_output=True, text=True, timeout=timeout,
                cwd=os.path.dirname(script)
            )
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"NotebookLM error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logger.error(f"NotebookLM timeout after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"NotebookLM failed: {e}")
            return None

    # ──────────────────────────────────────────
    # Docling Bridge (Local Fallback)
    # ──────────────────────────────────────────

    def docling_available(self) -> bool:
        """Check if Docling is installed."""
        try:
            import docling
            return True
        except ImportError:
            return False

    def install_docling(self, progress_cb: Optional[Callable] = None) -> bool:
        """Install Docling package."""
        try:
            if progress_cb:
                progress_cb(10, "Đang cài đặt Docling...")

            subprocess.run(
                [sys.executable, "-m", "pip", "install", "docling"],
                capture_output=True, timeout=120
            )

            if progress_cb:
                progress_cb(100, "Docling sẵn sàng!")
            return True
        except Exception as e:
            logger.error(f"Failed to install Docling: {e}")
            return False

    def docling_convert(self, pdf_path: str) -> Optional[str]:
        """Convert PDF to Markdown via Docling.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown content or None on failure
        """
        try:
            from docling.document_converter import DocumentConverter
            converter = DocumentConverter()
            result = converter.convert(pdf_path)
            return result.document.export_to_markdown()
        except Exception as e:
            logger.error(f"Docling failed: {e}")
            return None

    # ──────────────────────────────────────────
    # Auto Pipeline
    # ──────────────────────────────────────────

    def convert_document(self, pdf_path: str, prefer_cloud: bool = True) -> dict:
        """Convert PDF to Markdown with auto fallback.

        Args:
            pdf_path: Path to PDF
            prefer_cloud: Try NotebookLM first, fallback Docling

        Returns:
            dict with keys: success, markdown, method, error
        """
        if prefer_cloud and self.notebooklm_available():
            markdown = self.notebooklm_convert(pdf_path)
            if markdown:
                return {"success": True, "markdown": markdown, "method": "notebooklm"}
            logger.info("NotebookLM failed, falling back to Docling")

        if self.docling_available():
            markdown = self.docling_convert(pdf_path)
            if markdown:
                return {"success": True, "markdown": markdown, "method": "docling"}

        return {"success": False, "markdown": None, "method": None,
                "error": "No conversion method available"}
