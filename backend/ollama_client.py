"""Backend: Ollama Client — Manages local AI operations.

Handles Ollama API calls, model management, and embedding generation.
Checks and starts Ollama service if needed.

Wing: smartdoc_backend
Topic: ai_integration
Last Updated: 2026-05-05 09:05
"""

import requests
import subprocess
import time
from typing import Dict, Any, Optional, List


class OllamaClient:
    """Client for interacting with Ollama local AI service."""

    def __init__(self, host: str = "http://localhost:11434", model: str = "gemma4:e2b"):
        """Initialize Ollama client.

        Args:
            host: Ollama server URL
            model: LLM model name (gemma4:e2b, llama3.2, etc.)
        """
        self.host = host
        self.model = model
        self.timeout = 60

        # System prompts for different tasks
        self.system_prompts = {
            'metadata_extraction': "<|think|> You are a professional document standardization expert. Read Markdown from Docling and extract Metadata with 100% accuracy. Focus on title, date, author, and document type.",
            'document_refinement': "<|think|> You are a professional document editor. Improve the clarity, professionalism, and accuracy of the document while preserving the original meaning. Use thinking mode to reason through improvements before final output.",
            'rag_qa': "<|think|> You are an AI assistant helping users find information in documents. Answer questions based on the provided context. Use Vietnamese language and keep responses concise and easy to understand.",
            'summary': "<|think|> You are an expert at document summarization. Create clear, concise summaries that capture the key points.",
            'formalization': "<|think|> You are a professional writer. Rewrite the document in a formal, professional tone suitable for business communications.",
        }

    def is_running(self) -> bool:
        """Check if Ollama service is running.

        Returns:
            True if running, False otherwise
        """
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def start_ollama(self) -> bool:
        """Attempt to start Ollama service.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to start Ollama (Windows)
            subprocess.Popen(['ollama', 'serve'], shell=True, creationflags=subprocess.DETACHED_PROCESS)
            time.sleep(5)  # Wait for startup
            return self.is_running()
        except Exception as e:
            print(f"Failed to start Ollama: {e}")
            return False

    def ensure_running(self) -> bool:
        """Ensure Ollama is running, start if needed.

        Returns:
            True if running, False otherwise
        """
        if self.is_running():
            return True
        return self.start_ollama()

    def chat(self, prompt: str, task: str = 'rag_qa', context: Optional[List[str]] = None, images: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate chat completion with Gemma 4.

        Args:
            prompt: User prompt
            task: Task type (metadata_extraction, document_refinement, rag_qa, summary, formalization)
            context: Optional context documents
            images: Optional list of image paths for multimodal input

        Returns:
            Response with generated text
        """
        if not self.is_running():
            self.start_ollama()

        # Build messages
        messages = []

        # Add system prompt for the task
        if task in self.system_prompts:
            messages.append({
                "role": "system",
                "content": self.system_prompts[task]
            })

        # Add context if provided
        if context:
            context_text = "\n\n".join(context)
            messages.append({
                "role": "system",
                "content": f"Reference documents:\n{context_text}"
            })

        # Add user message
        user_message = {"role": "user", "content": prompt}

        # Add images for multimodal support
        if images and len(images) > 0:
            user_message["images"] = images

        messages.append(user_message)

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_ctx": 4096,  # Context window
                "temperature": 0.7,
            }
        }

        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def list_models(self) -> List[str]:
        """Get list of available Ollama models.

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=10)
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except:
            return []

    def pull_model(self, model_name: str) -> bool:
        """Download model if not available.

        Args:
            model_name: Name of model to pull

        Returns:
            True if successful
        """
        try:
            payload = {"name": model_name, "stream": False}
            response = requests.post(
                f"{self.host}/api/pull",
                json=payload,
                timeout=300  # 5 minutes timeout for download
            )
            return response.status_code == 200
        except:
            return False

    def ensure_model(self, model_name: Optional[str] = None) -> bool:
        """Ensure model is available, download if needed.

        Args:
            model_name: Name of model (uses default if None)

        Returns:
            True if model is available
        """
        check_model = model_name or self.model
        models = self.list_models()
        if check_model in models:
            return True
        return self.pull_model(check_model)
