const express = require('express');
const cors = require('cors');

const app = express();
const port = 8080;

app.use(cors())

app.get('/get-data', (req, res) => {
    res.send('test message');
})

app.listen(port, () => {
    console.log('Server listening on port:', port);
})

