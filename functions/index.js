const functions = require('firebase-functions');
const { spawn } = require('child_process');
const express = require('express');
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'public')));

app.all('/*', (req, res) => {
    const pythonProcess = spawn('python3', [path.resolve(__dirname, '../board/__init__.py')]);

    pythonProcess.stdout.on('data', (data) => {
        res.send(data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

exports.app = functions.https.onRequest(app);
