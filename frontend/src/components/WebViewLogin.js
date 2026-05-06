const React = require('react');

class WebViewLogin extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            status: 'idle',
            session: null,
            error: null,
        };
    }

    componentDidMount() {
        this.checkSession();
    }

    async checkSession() {
        if (!window.electronAPI) return;
        try {
            const session = await window.electronAPI.getLoginSession(this.props.service);
            this.setState({ session });
        } catch {}
    }

    async handleLogin() {
        if (!window.electronAPI) {
            this.setState({ error: 'electronAPI not available' });
            return;
        }

        this.setState({ status: 'logging', error: null });

        try {
            const result = await window.electronAPI.openLoginWindow({
                url: this.props.loginUrl,
                service: this.props.service,
                width: this.props.width || 800,
                height: this.props.height || 700,
            });

            if (result && result.cookies && result.cookies.length > 0) {
                this.setState({ status: 'success', session: result });
                if (this.props.onLogin) this.props.onLogin(result);
            } else {
                this.setState({ status: 'failed', error: 'Không tìm thấy session. Bạn đã đăng nhập thành công?' });
            }
        } catch (err) {
            this.setState({ status: 'failed', error: err.message });
        }
    }

    async handleClear() {
        if (!window.electronAPI) return;
        await window.electronAPI.clearLoginSession(this.props.service);
        this.setState({ session: null, status: 'idle' });
        if (this.props.onLogout) this.props.onLogout();
    }

    render() {
        const { status, session, error } = this.state;
        const { service, icon, compact } = this.props;

        if (compact) {
            return (
                <div className="flex items-center gap-2">
                    {session ? (
                        <>
                            <span className="w-2 h-2 rounded-full bg-emerald-400" />
                            <span className="text-xs text-emerald-600">Đã đăng nhập</span>
                            <button onClick={() => this.handleClear()}
                                className="text-[10px] text-red-400 hover:text-red-600 underline">
                                Thoát
                            </button>
                        </>
                    ) : (
                        <>
                            <span className="w-2 h-2 rounded-full bg-gray-300" />
                            <span className="text-xs text-gray-400">Chưa đăng nhập</span>
                            <button onClick={() => this.handleLogin()}
                                disabled={status === 'logging'}
                                className="text-[10px] text-primary-500 hover:text-primary-700 underline">
                                {status === 'logging' ? 'Đang đăng nhập...' : 'Đăng nhập'}
                            </button>
                        </>
                    )}
                </div>
            );
        }

        return (
            <div className="p-5 bg-white rounded-xl border border-gray-200 shadow-sm animate-slide-up">
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary-100 to-accent-50 rounded-xl flex items-center justify-center">
                        <span className="text-xl">{icon || '\u{1F510}'}</span>
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-gray-800">{service}</h3>
                        <p className="text-xs text-gray-400">Đăng nhập để sử dụng dịch vụ</p>
                    </div>
                    {session && (
                        <span className="ml-auto px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-700 text-[10px] font-medium">
                            {'\u2705'} Đã kết nối
                        </span>
                    )}
                </div>

                {error && (
                    <div className="mb-3 p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-700">
                        {error}
                    </div>
                )}

                <div className="flex gap-2">
                    {!session ? (
                        <button onClick={() => this.handleLogin()}
                            disabled={status === 'logging'}
                            className={`px-4 py-2 rounded-lg text-xs font-medium transition-all active:scale-95 ${
                                status === 'logging'
                                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                    : 'bg-primary-600 text-white hover:bg-primary-700'
                            }`}>
                            {status === 'logging' ? '\u23F3' : '\u{1F310}'} Đăng nhập {service}
                        </button>
                    ) : (
                        <button onClick={() => this.handleClear()}
                            className="px-4 py-2 rounded-lg text-xs font-medium bg-red-50 text-red-600 hover:bg-red-100 border border-red-200 transition-all">
                            {'\u{1F510}'} Thoát tài khoản
                        </button>
                    )}
                </div>

                <div className="mt-3 text-[10px] text-gray-400 leading-relaxed">
                    {'\u2139\uFE0F'} Cửa sổ đăng nhập sẽ mở ra. Sau khi đăng nhập thành công,
                    bạn có thể đóng cửa sổ đó lại. Session sẽ được lưu tự động.
                </div>
            </div>
        );
    }
}

module.exports = WebViewLogin;
