/**
 * Frontend: TabRag Component — RAG chat interface.
 *
 * Tab 3: Chat with AI using document context.
 * Displays sources and citations from retrieved documents.
 *
 * Wing: smartdoc_frontend
 * Topic: ui_components
 * Last Updated: 2026-05-05 09:47
 */

const React = require('react');
const ApiService = require('../services/api').default;

class TabRag extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            messages: [],
            inputMessage: '',
            loading: false,
        };
    }

    handleSendMessage() {
        const { inputMessage, messages } = this.state;

        if (!inputMessage.trim()) {
            return;
        }

        // Add user message
        const newMessages = [
            ...messages,
            { role: 'user', content: inputMessage },
        ];

        this.setState({
            messages: newMessages,
            inputMessage: '',
            loading: true,
        });

        // Get document context
        const context = this.props.documents.map(doc => doc.markdown);

        // Call AI
        ApiService.chat(inputMessage, context)
            .then((response) => {
                const aiMessage = response.message?.content || 'Xin lỗi, có lỗi xảy ra.';

                this.setState({
                    messages: [
                        ...newMessages,
                        { role: 'assistant', content: aiMessage },
                    ],
                    loading: false,
                });
            })
            .catch((error) => {
                this.setState({
                    messages: [
                        ...newMessages,
                        { role: 'assistant', content: `Lỗi: ${error.message}` },
                    ],
                    loading: false,
                });
            });
    }

    handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.handleSendMessage();
        }
    }

    render() {
        const { messages, inputMessage, loading } = this.state;

        return (
            <div className="flex flex-col h-full">
                {/* Chat Messages */}
                <div className="flex-1 overflow-auto p-6 bg-background">
                    <div className="max-w-4xl mx-auto space-y-4">
                        {messages.length === 0 && (
                            <div className="text-center py-12">
                                <div className="text-6xl mb-4">💬</div>
                                <h3 className="text-xl font-semibold text-gray-800">
                                    Hỏi đáp với Tài liệu của bạn
                                </h3>
                                <p className="text-gray-600 mt-2">
                                    Hãy đặt câu hỏi về các tài liệu đã được lưu vào kho
                                </p>
                            </div>
                        )}

                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-2xl p-4 rounded-lg ${
                                        msg.role === 'user'
                                            ? 'bg-primary text-white'
                                            : 'bg-white border shadow-sm'
                                    }`}
                                >
                                    {msg.role === 'assistant' && (
                                        <div className="text-sm font-medium text-primary mb-2">
                                            🤖 AI Assistant
                                        </div>
                                    )}
                                    <div className="whitespace-pre-wrap text-base">
                                        {msg.content}
                                    </div>
                                    {msg.role === 'assistant' && (
                                        <div className="mt-3 pt-3 border-t">
                                            <button className="text-sm text-primary hover:underline">
                                                👁️ Xem tài liệu gốc
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}

                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-white border shadow-sm p-4 rounded-lg">
                                    <div className="flex items-center gap-2">
                                        <div className="animate-spin">⏳</div>
                                        <span>AI đang suy nghĩ...</span>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Input Area */}
                <div className="border-t bg-white p-4">
                    <div className="max-w-4xl mx-auto flex gap-2">
                        <textarea
                            value={inputMessage}
                            onChange={(e) => this.setState({ inputMessage: e.target.value })}
                            onKeyPress={(e) => this.handleKeyPress(e)}
                            placeholder="Nhập câu hỏi của bạn..."
                            className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-primary resize-none"
                            rows="3"
                            disabled={loading}
                        ></textarea>
                        <button
                            onClick={() => this.handleSendMessage()}
                            disabled={loading || !inputMessage.trim()}
                            className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed self-end"
                        >
                            Gửi
                        </button>
                    </div>
                </div>

                {/* Source Info */}
                <div className="border-t bg-gray-50 p-2">
                    <div className="max-w-4xl mx-auto text-sm text-gray-600">
                        📚 Nguồn dữ liệu: {this.props.documents.length} tài liệu đã lưu
                    </div>
                </div>
            </div>
        );
    }
}

module.exports = TabRag;
