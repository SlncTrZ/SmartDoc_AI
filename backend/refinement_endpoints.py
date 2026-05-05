"""Backend: Add document refinement endpoints to Flask app.

Provides API endpoints for AI-powered document improvement using Gemma 4.
"""

from flask import request, jsonify
import logging
logger = logging.getLogger(__name__)

@app.route('/api/refine/summarize', methods=['POST'])
def summarize_document():
    """Generate summary of document."""
    data = request.json
    markdown = data.get('markdown')

    if not markdown:
        return jsonify({'error': 'Markdown content required'}), 400

    try:
        summary = document_refiner.summarize(markdown)
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        logger.error(f"Summary error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/refine/formalize', methods=['POST'])
def formalize_document():
    """Rewrite document in formal tone."""
    data = request.json
    markdown = data.get('markdown')

    if not markdown:
        return jsonify({'error': 'Markdown content required'}), 400

    try:
        formalized = document_refiner.formalize(markdown)
        return jsonify({
            'success': True,
            'markdown': formalized
        })
    except Exception as e:
        logger.error(f"Formalization error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/refine/custom', methods=['POST'])
def custom_refinement():
    """Apply custom refinement to document."""
    data = request.json
    markdown = data.get('markdown')
    instruction = data.get('instruction')

    if not markdown or not instruction:
        return jsonify({'error': 'Markdown and instruction required'}), 400

    try:
        refined = document_refiner.custom_refinement(markdown, instruction)
        return jsonify({
            'success': True,
            'markdown': refined
        })
    except Exception as e:
        logger.error(f"Custom refinement error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/refine/tables', methods=['POST'])
def extract_tables():
    """Extract tables from document."""
    data = request.json
    markdown = data.get('markdown')

    if not markdown:
        return jsonify({'error': 'Markdown content required'}), 400

    try:
        tables = document_refiner.extract_tables(markdown)
        return jsonify({
            'success': True,
            'tables': tables
        })
    except Exception as e:
        logger.error(f"Table extraction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/refine/structure', methods=['POST'])
def improve_structure():
    """Improve document structure and formatting."""
    data = request.json
    markdown = data.get('markdown')

    if not markdown:
        return jsonify({'error': 'Markdown content required'}), 400

    try:
        improved = document_refiner.improve_structure(markdown)
        return jsonify({
            'success': True,
            'markdown': improved
        })
    except Exception as e:
        logger.error(f"Structure improvement error: {e}")
        return jsonify({'error': str(e)}), 500
