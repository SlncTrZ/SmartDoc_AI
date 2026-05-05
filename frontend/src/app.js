/**
 * Frontend: Main React App — Entry point for SmartDoc AI.
 *
 * Initializes React app with 3-tab interface.
 * Tab 1: Input & Scan
 * Tab 2: Preview & Refine
 * Tab 3: RAG Chat
 *
 * Wing: smartdoc_frontend
 * Topic: main_app
 * Last Updated: 2026-05-05 09:45
 */

const React = require('react');
const ReactDOM = require('react-dom/client');
const App = require('./components/App').default;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
