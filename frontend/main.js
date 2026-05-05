/**
 * Frontend: Electron Main Process — Entry point for Electron app.
 *
 * Creates main window, handles file operations, manages Python subprocess.
 * Starts Python Flask server on app launch.
 *
 * Wing: smartdoc_frontend
 * Topic: electron_main
 * Last Updated: 2026-05-05 09:47
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow = null;
let pythonProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 1024,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js'),
        },
        icon: path.join(__dirname, '../assets/icon.png'),
    });

    // Load the index.html
    mainWindow.loadFile(path.join(__dirname, '../public/index.html'));

    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function startPythonServer() {
    const pythonPath = path.join(__dirname, '../../backend/venv/Scripts/python.exe');
    const scriptPath = path.join(__dirname, '../../backend/app.py');

    pythonProcess = spawn(pythonPath, [scriptPath], {
        cwd: path.join(__dirname, '../../backend'),
        detached: false,
    });

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python server exited with code ${code}`);
    });
}

app.whenReady().then(() => {
    // Start Python server first
    console.log('Starting Python backend server...');
    startPythonServer();

    // Wait a bit for Python to start, then create window
    setTimeout(() => {
        createWindow();
    }, 3000);

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        // Kill Python server when closing app
        if (pythonProcess) {
            pythonProcess.kill();
        }
        app.quit();
    }
});

// IPC handlers for file operations
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
