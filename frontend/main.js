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

const { app, BrowserWindow, ipcMain, session } = require('electron');
const path = require('path');
const fs = require('fs');
const SidecarManager = require('./src/main/sidecar-manager');

let mainWindow = null;
let sidecar = null;
let backendPort = null;
let loginWindow = null;

const SESSION_DIR = path.join(app.getPath('userData'), 'sessions');

function ensureSessionDir() {
    if (!fs.existsSync(SESSION_DIR)) {
        fs.mkdirSync(SESSION_DIR, { recursive: true });
    }
}

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

    // ─── WebView Login ───
    ipcMain.handle('open-login-window', async (_event, { url, service, width = 800, height = 700 }) => {
        ensureSessionDir();

        return new Promise((resolve) => {
            if (loginWindow) {
                loginWindow.close();
            }

            loginWindow = new BrowserWindow({
                width,
                height,
                title: `Đăng nhập ${service}`,
                webPreferences: {
                    nodeIntegration: false,
                    contextIsolation: true,
                    webSecurity: false,
                },
                parent: mainWindow,
                modal: true,
                show: false,
                backgroundColor: '#ffffff',
            });

            const sessionPath = path.join(SESSION_DIR, `${service.toLowerCase().replace(/\s+/g, '_')}.json`);
            let navigated = false;

            loginWindow.webContents.on('did-navigate', async () => {
                navigated = true;
            });

            loginWindow.webContents.on('did-navigate-in-page', async () => {
                navigated = true;
            });

            const tryExtractCookies = async () => {
                try {
                    const cookies = await loginWindow.webContents.session.cookies.get({});
                    const loginUrl = loginWindow.webContents.getURL();

                    const sessionData = {
                        service,
                        url: loginUrl,
                        cookies,
                        timestamp: Date.now(),
                    };

                    fs.writeFileSync(sessionPath, JSON.stringify(sessionData, null, 2));
                    return sessionData;
                } catch {
                    return null;
                }
            };

            loginWindow.on('close', async () => {
                const sessionData = await tryExtractCookies();
                loginWindow = null;
                resolve(sessionData || { service, cookies: [], url: '' });
            });

            loginWindow.loadURL(url);
            loginWindow.once('ready-to-show', () => {
                loginWindow.show();
            });

            setTimeout(async () => {
                if (loginWindow && !navigated) {
                    const sessionData = await tryExtractCookies();
                    if (sessionData && sessionData.cookies.length > 0) {
                        loginWindow.close();
                    }
                }
            }, 60000);
        });
    });

    ipcMain.handle('get-login-session', async (_event, service) => {
        ensureSessionDir();
        const sessionPath = path.join(SESSION_DIR, `${service.toLowerCase().replace(/\s+/g, '_')}.json`);
        try {
            const data = fs.readFileSync(sessionPath, 'utf-8');
            return JSON.parse(data);
        } catch {
            return null;
        }
    });

    ipcMain.handle('clear-login-session', async (_event, service) => {
        ensureSessionDir();
        const sessionPath = path.join(SESSION_DIR, `${service.toLowerCase().replace(/\s+/g, '_')}.json`);
        try {
            fs.unlinkSync(sessionPath);
            return true;
        } catch {
            return false;
        }
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
