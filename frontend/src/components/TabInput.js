const React = require('react');

class TabInput extends React.Component {
    render() {
        const UploadZone = window.UploadZoneComponent;
        return UploadZone ? React.createElement(UploadZone, {
            onDocumentProcessed: this.props.onDocumentProcessed,
        }) : null;
    }
}

module.exports = TabInput;
