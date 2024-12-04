const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const logFile = path.join(__dirname, 'logs', 'app.log');

fs.mkdirSync(path.dirname(logFile), { recursive: true });

function log(message) {
    fs.appendFileSync(logFile, `${new Date().toISOString()} - ${message}\n`);
}

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
    if (req.method === 'POST') {
        log(`POST request to ${req.originalUrl} with body: ${JSON.stringify(req.body)}`);
    }
    next();
});

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', (req, res) => {
    res.render('index', { result: null, error: null });
});

app.post('/ping', (req, res) => {
    const host = req.body.hostname;

    exec(`ping -c 3 ${host}`, (error, stdout, stderr) => {
        if (error) {
            res.render('index', { result: null, error: stderr });
            return;
        }
        res.render('index', { result: stdout, error: null });
    });
});

if (require.main === module) {
    const server = app.listen(3000, () => {
        console.log(`Server running on http://localhost:3000`);
    });
}

module.exports = app;

