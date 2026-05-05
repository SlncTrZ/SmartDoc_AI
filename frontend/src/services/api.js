/**
 * Frontend: API Service — Handles communication with Python backend.
 *
 * Provides methods for file processing, storage, and RAG operations.
 * Uses fetch API to communicate with Flask server on port 5000.
 *
 * Wing: smartdoc_frontend
 * Topic: api_service
 * Last Updated: 2026-05-05 09:45
 */

const API_BASE_URL = 'http://127.0.0.1:5000/api';

class ApiService {
    /**
     * Check backend health status
     */
    async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error', ollama_running: false };
        }
    }

    /**
     * Process a document file
     * @param {string} filePath - Full path to the file
     */
    async processFile(filePath) {
        try {
            const response = await fetch(`${API_BASE_URL}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ file_path: filePath }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Processing failed');
            }

            return data;
        } catch (error) {
            console.error('File processing failed:', error);
            throw error;
        }
    }

    /**
     * Get list of all wings (categories)
     */
    async getWings() {
        try {
            const response = await fetch(`${API_BASE_URL}/wings`);
            return await response.json();
        } catch (error) {
            console.error('Failed to get wings:', error);
            return [];
        }
    }

    /**
     * Start Ollama service
     */
    async startOllama() {
        try {
            const response = await fetch(`${API_BASE_URL}/ollama/start`, {
                method: 'POST',
            });
            return await response.json();
        } catch (error) {
            console.error('Failed to start Ollama:', error);
            return { success: false };
        }
    }

    /**
     * Chat with AI
     * @param {string} message - User message
     * @param {string[]} context - Document context
     */
    async chat(message, context = []) {
        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message, context }),
            });

            return await response.json();
        } catch (error) {
            console.error('Chat failed:', error);
            throw error;
        }
    }
}

module.exports = new ApiService();
