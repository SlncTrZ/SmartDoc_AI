const React = require('react');
const UploadZone = require('./UploadZone').default;

class TabInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mode: props.operationMode || 'hybrid',
        };
    }

    handleModeToggle(newMode) {
        this.setState({ mode: newMode });
    }

    render() {
        return (
            <UploadZone
                operationMode={this.state.mode}
                onModeToggle={(m) => this.handleModeToggle(m)}
                onDocumentProcessed={this.props.onDocumentProcessed}
            />
        );
    }
}

module.exports = TabInput;
