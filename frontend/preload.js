/**
 * Frontend: Preload Script — Expose safe APIs to renderer process.
 *
 * Provides IPC bridge between main process and renderer.
 * Exposes file dialog and other system APIs safely.
 *
 * Wing: smartdoc_frontend
 * Topic: electron_security
 * Last Updated: 2026-05-05 09:48
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
});
