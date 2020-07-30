const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');
const sha256 = require('js-sha256');
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

const calculateAuthCode = (req) => {
    const authCodeString = '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ' + req.body.authCodeString;
    return { authcode: sha256.hex(authCodeString).toUpperCase() };
};

app.post('/authcode', (req, res) => res.send(calculateAuthCode(req)));

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));
