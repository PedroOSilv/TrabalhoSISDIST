const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const multer  = require('multer');
const fs = require('fs');

const app = express();
const port = 3000;

// Configuração do multer para onde os arquivos serão salvos
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      // O diretório onde os arquivos serão salvos
      const uploadDir = path.join(__dirname, 'uploads');
      // Cria o diretório se não existir
      fs.mkdirSync(uploadDir, { recursive: true });
      cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
      // Define o nome do arquivo
      cb(null, file.originalname); // Você pode alterar o nome conforme necessário
    }
  });

// Opções do multer
const upload = multer({ storage: storage })

// Servir arquivos estáticos da pasta 'web-app'
app.use(express.static(path.join(__dirname, 'website')));

// Rota POST para lidar com o upload do arquivo
app.post('/upload', upload.single('file'), (req, res) => {
    if (req.file) {
        // Extrai o nome do arquivo
        const fileName = req.file.originalname;

        // Constrói a string de comando com o nome do arquivo
        const command = `python3 client/clientUpload.py "uploads/${fileName}" "${fileName}"`;

        // Executa o script Python com o nome do arquivo como parâmetro
        exec(command, (error, stdout, stderr) => {
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
    } else {
        res.status(400).send('Nenhum arquivo foi enviado.');
    }
});

app.get('/run-python', (req, res) => {
    // Extrai parâmetros da query string. Exemplo: /run-python?param1=value1&param2=value2
    const params = Object.entries(req.query)
                         .map(([key, value]) => `${key}=${value}`)
                         .join(' ');

    // Constrói a string de comando com os parâmetros
    const command = `python3 script.py ${params}`;

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
