/**
 * Frontend: Electron Main Process — Entry point for Electron app.
 *
 * Creates main window, manages sidecar processes.
 * Dynamic port allocation to avoid conflicts.
 *
 * Wing: smartdoc_frontend
 * Topic: electron_main
 * Last Updated: 2026-05-06
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const SidecarManager = require('./src/main/sidecar-manager');

let mainWindow = null;
let sidecar = null;
let backendPort = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 860,
        minWidth: 1024,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js'),
            webSecurity: false,
        },
        icon: path.join(__dirname, '../assets/icon.png'),
        show: false,
        backgroundColor: '#0f172a',
    });

    mainWindow.loadFile(path.join(__dirname, 'public/index.html'));

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        mainWindow.webContents.openDevTools();
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function setupSidecar() {
    sidecar = new SidecarManager();

    ipcMain.handle('get-backend-port', () => backendPort);

    ipcMain.handle('hardware-check', async () => {
        try {
            const output = await sidecar.runOnce('hardware-check', 'hardware_check.py');
            try {
                return JSON.parse(output);
            } catch {
                return { status: 'ok', gpu: { gpu_detected: false, recommended_mode: 'hybrid' } };
            }
        } catch (error) {
            return { status: 'error', error: error.message, gpu: { gpu_detected: false, recommended_mode: 'hybrid' } };
        }
    });

    ipcMain.handle('sidecar-status', async () => {
        return sidecar ? sidecar.getStatus() : {};
    });

    ipcMain.handle('sidecar-health', async (_event, name) => {
        return sidecar ? sidecar.healthCheck(name) : false;
    });

    ipcMain.handle('sidecar-stop', async (_event, name) => {
        if (sidecar) return sidecar.stop(name);
        return false;
    });

    ipcMain.handle('open-file-dialog', async () => {
        const { dialog } = require('electron');
        const result = await dialog.showOpenDialog({
            properties: ['openFile', 'multiSelections'],
            filters: [{ name: 'PDF Files', extensions: ['pdf'] }],
        });
        if (!result.canceled && result.filePaths.length > 0) {
            return result.filePaths;
        }
        return [];
    });
}

async function startBackend() {
    backendPort = await sidecar.findFreePort(5000);
    console.log(`[Main] Starting Flask backend on port ${backendPort}...`);
    try {
        await sidecar.start('flask-backend', 'app.py', {
            port: backendPort,
            args: ['--port', String(backendPort)],
        });
        console.log('[Main] Flask backend ready on port', backendPort);
    } catch (error) {
        console.error('[Main] Failed to start Flask backend:', error.message);
    }
}

async function initApp() {
    setupSidecar();
    await startBackend();
    createWindow();
}

app.whenReady().then(initApp);

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        initApp();
    }
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    if (sidecar) sidecar.stopAll();
});
