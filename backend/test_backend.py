"""Backend: Test Suite — Tests for document processing and storage.

Unit tests for Docling extraction, LanceDB operations, and API endpoints.
Run with: python -m pytest backend/tests/

Wing: smartdoc_backend
Topic: testing
Last Updated: 2026-05-05 09:05
"""

import pytest
import os
from pathlib import Path
from processor import DocumentProcessor
from vector_storage import VectorStorage
from ollama_client import OllamaClient


class TestDocumentProcessor:
    """Tests for DocumentProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return DocumentProcessor()

    def test_processor_initialization(self, processor):
        """Test processor initialization."""
        assert processor.converter is not None

    def test_process_nonexistent_file(self, processor):
        """Test processing non-existent file."""
        result = processor.process_file('nonexistent.pdf')
        assert result['success'] is False


class TestVectorStorage:
    """Tests for VectorStorage class."""

    @pytest.fixture
    def storage(self, tmp_path):
        """Create storage instance with temp path."""
        db_path = str(tmp_path / "test_db")
        return VectorStorage(db_path)

    def test_storage_initialization(self, storage):
        """Test storage initialization."""
        assert storage.db is not None
        assert os.path.exists(storage.db_path)

    def test_create_wing(self, storage):
        """Test creating a new wing."""
        storage.create_wing('test_wing')
        wings = storage.list_wings()
        assert 'test_wing' in wings

    def test_ensure_wings(self, storage):
        """Test ensuring default wings exist."""
        storage.ensure_wings(['wing1', 'wing2'])
        wings = storage.list_wings()
        assert 'wing1' in wings
        assert 'wing2' in wings


class TestOllamaClient:
    """Tests for OllamaClient class."""

    @pytest.fixture
    def client(self):
        """Create client instance."""
        return OllamaClient()

    def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.host == "http://localhost:11434"
        assert client.timeout == 60

    def test_is_running(self, client):
        """Test checking if Ollama is running."""
        # Just ensure method doesn't crash
        result = client.is_running()
        assert isinstance(result, bool)


class TestAPIEndpoints:
    """Integration tests for Flask API."""

    @pytest.fixture
    def client(self):
        """Create Flask test client."""
        from app import app
        app.config['TESTING'] = True
        return app.test_client()

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data

    def test_list_wings(self, client):
        """Test list wings endpoint."""
        response = client.get('/api/wings')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
