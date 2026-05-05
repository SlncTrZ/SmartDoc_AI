/**
 * Frontend: Build Script — Bundle React components for Electron.
 *
 * Simple bundler that doesn't require Webpack/Vite.
 * Uses Node.js built-in modules to create app.js bundle.
 *
 * Wing: smartdoc_frontend
 * Topic: build_tools
 * Last Updated: 2026-05-05 09:48
 */

const fs = require('fs');
const path = require('path');

function bundleReact() {
    console.log('Building React components...');

    // Simple bundler - just copy files and add exports
    const componentsDir = path.join(__dirname, 'src/components');
    const servicesDir = path.join(__dirname, 'src/services');
    const outputDir = path.join(__dirname, 'public');
    const outputPath = path.join(outputDir, 'app.js');

    let bundleContent = `
// React Bundle
const React = require('react');
const ReactDOM = require('react-dom');

// Components
${readComponents(componentsDir)}

// Services
${readServices(servicesDir)}

// Initialize app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    React.createElement(React.StrictMode, null,
        React.createElement(App, null)
    )
);
console.log('SmartDoc AI loaded successfully!');
`;

    fs.writeFileSync(outputPath, bundleContent);
    console.log('React bundle created: app.js');
}

function readComponents(dir) {
    let content = '';

    const files = fs.readdirSync(dir);
    files.forEach(file => {
        if (file.endsWith('.js')) {
            const filePath = path.join(dir, file);
            const fileContent = fs.readFileSync(filePath, 'utf-8');

            // Extract class name and export
            const match = fileContent.match(/class (\w+)/);
            const className = match ? match[1] : file.replace('.js', '');

            content += `
// ${file}
(function() {
${fileContent}

module.exports = ${className};
})();
`;
        }
    });

    return content;
}

function readServices(dir) {
    let content = '';

    const files = fs.readdirSync(dir);
    files.forEach(file => {
        if (file.endsWith('.js')) {
            const filePath = path.join(dir, file);
            const fileContent = fs.readFileSync(filePath, 'utf-8');
            content += `
// ${file}
${fileContent}
`;
        }
    });

    return content;
}

bundleReact();
