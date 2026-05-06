const React = require('react');

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
        const UploadZone = window.UploadZoneComponent;
        return UploadZone ? React.createElement(UploadZone, {
            operationMode: this.state.mode,
            onModeToggle: (m) => this.handleModeToggle(m),
            onDocumentProcessed: this.props.onDocumentProcessed,
        }) : null;
    }
}

module.exports = TabInput;
