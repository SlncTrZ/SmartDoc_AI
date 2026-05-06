"""ds2api Client — Bridge to DeepSeek via web interface.

Sidecar service: spawns ds2api FastAPI server.
Fallback: direct requests to ds2api local endpoint.

Wing: smartdoc_backend
Topic: ai_integration
Updated: 2026-05-06
"""

import os
import json
import requests
from typing import Optional


class DS2APIClient:
    """Client for ds2api service."""

    def __init__(self, base_url: str = "http://127.0.0.1:9090"):
        self.base_url = base_url
        self.session_file = os.path.join(
            os.environ.get("APPDATA", os.path.expanduser("~")),
            "SmartDoc_AI", "ds2api_session.json"
        )

    def _ensure_session_dir(self):
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)

    def save_session(self, cookies: dict):
        self._ensure_session_dir()
        with open(self.session_file, "w") as f:
            json.dump({"cookies": cookies}, f)

    def load_session(self) -> Optional[dict]:
        try:
            with open(self.session_file, "r") as f:
                data = json.load(f)
                return data.get("cookies")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=3)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def chat(self, messages: list, model: str = "deepseek-chat") -> Optional[str]:
        """Send chat request to ds2api.

        Args:
            messages: List of {"role": "user"/"assistant", "content": "..."}
            model: Model name (deepseek-chat or deepseek-reasoner)

        Returns:
            Response text or None on error
        """
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
            }
            r = requests.post(f"{self.base_url}/v1/chat/completions",
                              json=payload, timeout=60)
            if r.status_code == 200:
                data = r.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content")
            return None
        except requests.RequestException as e:
            print(f"[ds2api] Chat error: {e}")
            return None

    def get_available_models(self) -> list:
        try:
            r = requests.get(f"{self.base_url}/v1/models", timeout=5)
            if r.status_code == 200:
                data = r.json()
                return [m["id"] for m in data.get("data", [])]
        except requests.RequestException:
            pass
        return ["deepseek-chat", "deepseek-reasoner"]
