const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const port = 5000;
app.use(express.json());

app.use(cors())

app.post('/process-image', (req, res) => {

    const {imageURL} = req.body;
    const pythonProcess = spawn('python', ['./data-manipulation/main.py ', imageURL]);

    let result = '';
    pythonProcess.stdout.on('data', data => {
        result = data.toString();
    })
    pythonProcess.stderr.on('data', data => {
        result = data.toString();
    })

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.json({body:result});
        } else {
            res.status(500).json({error: result});
        }
    })

})

app.listen(port, () => {
    console.log('Server listening on port:', port);
})

