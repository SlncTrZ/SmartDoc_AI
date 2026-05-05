/**
 * Frontend: TabInput Component — File upload and processing interface.
 *
 * Tab 1: Drag & drop zone for PDF files.
 * Displays processing status and progress.
 *
 * Wing: smartdoc_frontend
 * Topic: ui_components
 * Last Updated: 2026-05-05 09:46
 */

const React = require('react');
const ApiService = require('../services/api').default;

class TabInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isDragging: false,
            files: [],
            processing: false,
            progress: 0,
            status: '',
        };
        this.fileInputRef = React.createRef();
    }

    handleDragOver(e) {
        e.preventDefault();
        this.setState({ isDragging: true });
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.setState({ isDragging: false });
    }

    handleDrop(e) {
        e.preventDefault();
        this.setState({ isDragging: false });

        const droppedFiles = Array.from(e.dataTransfer.files);
        this.handleFiles(droppedFiles);
    }

    handleFileSelect(e) {
        const selectedFiles = Array.from(e.target.files);
        this.handleFiles(selectedFiles);
    }

    async handleFiles(files) {
        const pdfFiles = files.filter(file => file.type === 'application/pdf');

        if (pdfFiles.length === 0) {
            alert('Vui lòng chọn file PDF');
            return;
        }

        this.setState({ files: pdfFiles });

        // Process files
        for (let i = 0; i < pdfFiles.length; i++) {
            const file = pdfFiles[i];
            this.setState({
                processing: true,
                progress: ((i) / pdfFiles.length) * 100,
                status: `Đang xử lý file ${i + 1}/${pdfFiles.length}: ${file.name}`,
            });

            try {
                // Get full path (Electron-specific)
                const filePath = file.path || file.name;

                const result = await ApiService.processFile(filePath);

                // Notify parent
                this.props.onDocumentProcessed({
                    filename: result.metadata.filename || file.name,
                    markdown: result.markdown,
                    metadata: result.metadata,
                    wing: result.wing,
                    filePath: filePath,
                });

            } catch (error) {
                console.error('Processing failed:', error);
                alert(`Lỗi xử lý file ${file.name}: ${error.message}`);
            }
        }

        this.setState({
            processing: false,
            progress: 100,
            status: 'Hoàn tất!',
        });
    }

    render() {
        const { isDragging, files, processing, progress, status } = this.state;

        return (
            <div className="container mx-auto p-6">
                <div className="max-w-4xl mx-auto">
                    <h2 className="text-2xl font-bold mb-6 text-gray-800">Tiếp nhận & Quét Tài liệu</h2>

                    {/* Drag & Drop Zone */}
                    <div
                        onDragOver={(e) => this.handleDragOver(e)}
                        onDragLeave={(e) => this.handleDragLeave(e)}
                        onDrop={(e) => this.handleDrop(e)}
                        onClick={() => this.fileInputRef.current.click()}
                        className={`border-4 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                            isDragging
                                ? 'border-primary bg-blue-50'
                                : 'border-gray-300 hover:border-primary hover:bg-gray-50'
                        } ${processing ? 'pointer-events-none opacity-50' : ''}`}
                    >
                        <input
                            ref={this.fileInputRef}
                            type="file"
                            multiple
                            accept=".pdf"
                            style={{ display: 'none' }}
                            onChange={(e) => this.handleFileSelect(e)}
                        />

                        {!processing && (
                            <div>
                                <div className="text-6xl mb-4">📄</div>
                                <h3 className="text-xl font-semibold mb-2">Kéo thả PDF vào đây</h3>
                                <p className="text-gray-600">hoặc nhấp để chọn file từ máy tính</p>
                            </div>
                        )}

                        {processing && (
                            <div>
                                <div className="text-6xl mb-4">⏳</div>
                                <h3 className="text-xl font-semibold mb-2">{status}</h3>
                                <div className="w-full bg-gray-200 rounded-full h-4 mt-4">
                                    <div
                                        className="bg-primary h-4 rounded-full transition-all duration-300"
                                        style={{ width: `${progress}%` }}
                                    ></div>
                                </div>
                                <p className="text-sm text-gray-600 mt-2">{progress.toFixed(0)}% hoàn thành</p>
                            </div>
                        )}
                    </div>

                    {/* File List */}
                    {files.length > 0 && !processing && (
                        <div className="mt-6">
                            <h3 className="text-lg font-semibold mb-3">Các file đã chọn:</h3>
                            <ul className="space-y-2">
                                {files.map((file, index) => (
                                    <li key={index} className="bg-white p-3 rounded shadow-sm flex items-center">
                                        <span className="text-2xl mr-3">📎</span>
                                        <span className="flex-1">{file.name}</span>
                                        <span className="text-gray-500 text-sm">
                                            {(file.size / 1024 / 1024).toFixed(2)} MB
                                        </span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

module.exports = TabInput;
