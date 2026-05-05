/**
 * Frontend: App Component — Main application with 3-tab interface.
 *
 * Manages tab navigation and overall app state.
 * Tab 1: Input & Scan (file upload)
 * Tab 2: Preview & Refine (document review)
 * Tab 3: RAG Chat (AI conversation)
 *
 * Wing: smartdoc_frontend
 * Topic: main_component
 * Last Updated: 2026-05-05 09:45
 */

const React = require('react');
const TabInput = require('./TabInput').default;
const TabPreview = require('./TabPreview').default;
const TabRag = require('./TabRag').default;
const ApiService = require('../services/api').default;

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeTab: 'input', // 'input', 'preview', 'rag'
            backendStatus: 'checking',
            ollamaRunning: false,
            documents: [],
            currentDocument: null,
        };
    }

    componentDidMount() {
        this.checkBackend();
        this.statusInterval = setInterval(() => this.checkBackend(), 30000);
    }

    componentWillUnmount() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
        }
    }

    async checkBackend() {
        try {
            const health = await ApiService.checkHealth();
            this.setState({
                backendStatus: health.status,
                ollamaRunning: health.ollama_running,
            });
        } catch (error) {
            this.setState({
                backendStatus: 'error',
                ollamaRunning: false,
            });
        }
    }

    handleTabChange(tab) {
        this.setState({ activeTab: tab });
    }

    handleDocumentProcessed(document) {
        this.setState(prevState => ({
            documents: [...prevState.documents, document],
            currentDocument: document,
            activeTab: 'preview',
        }));
    }

    handleStartOllama() {
        ApiService.startOllama();
    }

    render() {
        const { activeTab, backendStatus, ollamaRunning, documents, currentDocument } = this.state;

        return (
            <div className="flex flex-col h-screen bg-background">
                {/* Header */}
                <header className="bg-primary text-white p-4 shadow-md">
                    <div className="container mx-auto flex justify-between items-center">
                        <h1 className="text-xl font-bold">SmartDoc AI</h1>
                        <div className="flex items-center gap-4">
                            <span className="text-sm">
                                Backend: {backendStatus === 'healthy' ? '✓' : '✗'}
                            </span>
                            <span className="text-sm">
                                Ollama: {ollamaRunning ? '✓' : '✗'}
                            </span>
                            {!ollamaRunning && (
                                <button
                                    onClick={this.handleStartOllama}
                                    className="bg-warning text-black px-3 py-1 rounded text-sm hover:bg-yellow-500"
                                >
                                    Khởi động Ollama
                                </button>
                            )}
                        </div>
                    </div>
                </header>

                {/* Tab Navigation */}
                <nav className="bg-white border-b shadow-sm">
                    <div className="container mx-auto flex">
                        <button
                            onClick={() => this.handleTabChange('input')}
                            className={`flex-1 py-4 text-lg font-medium transition-colors ${
                                activeTab === 'input'
                                    ? 'bg-primary text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                        >
                            1. Tiếp nhận & Quét
                        </button>
                        <button
                            onClick={() => this.handleTabChange('preview')}
                            className={`flex-1 py-4 text-lg font-medium transition-colors ${
                                activeTab === 'preview'
                                    ? 'bg-primary text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                        >
                            2. Kiểm duyệt & Chỉnh sửa
                        </button>
                        <button
                            onClick={() => this.handleTabChange('rag')}
                            className={`flex-1 py-4 text-lg font-medium transition-colors ${
                                activeTab === 'rag'
                                    ? 'bg-primary text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                        >
                            3. Tra cứu & Hỏi đáp
                        </button>
                    </div>
                </nav>

                {/* Tab Content */}
                <main className="flex-1 overflow-auto">
                    {activeTab === 'input' && (
                        <TabInput onDocumentProcessed={(doc) => this.handleDocumentProcessed(doc)} />
                    )}
                    {activeTab === 'preview' && (
                        <TabPreview
                            document={currentDocument}
                            documents={documents}
                            onDocumentSelect={(doc) => this.setState({ currentDocument: doc })}
                        />
                    )}
                    {activeTab === 'rag' && (
                        <TabRag documents={documents} />
                    )}
                </main>

                {/* Status Bar */}
                <footer className="bg-gray-200 text-gray-700 p-2 text-sm border-t">
                    <div className="container mx-auto flex justify-between">
                        <span>Tài liệu đã xử lý: {documents.length}</span>
                        <span>SmartDoc AI v1.0</span>
                    </div>
                </footer>
            </div>
        );
    }
}

module.exports = App;
