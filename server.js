const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 3000;

// Servir arquivos estáticos da pasta 'web-app'
app.use(express.static(path.join(__dirname, 'website')));

// // Rota raiz para servir index.html
// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'website', 'indexProv.html'));
//   });

app.get('/run-python', (req, res) => {
    exec('python3 script.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).send(`Stderr: ${stderr}`);
        }
        res.send(`Output: ${stdout}`);
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
