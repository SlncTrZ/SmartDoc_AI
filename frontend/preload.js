const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
    hardwareCheck: () => ipcRenderer.invoke('hardware-check'),
    getBackendPort: () => ipcRenderer.invoke('get-backend-port'),
    getSidecarStatus: () => ipcRenderer.invoke('sidecar-status'),
    sidecarHealth: (name) => ipcRenderer.invoke('sidecar-health', name),
    sidecarStop: (name) => ipcRenderer.invoke('sidecar-stop', name),

    // WebView Login
    openLoginWindow: (opts) => ipcRenderer.invoke('open-login-window', opts),
    getLoginSession: (service) => ipcRenderer.invoke('get-login-session', service),
    clearLoginSession: (service) => ipcRenderer.invoke('clear-login-session', service),
});
