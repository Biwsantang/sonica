const yargs = require('yargs/yargs')
const { hideBin } = require('yargs/helpers')

const WebSocket = require('ws')
const serialport = require('serialport')
const Readline = require('@serialport/parser-readline')

const argv = yargs(hideBin(process.argv)).default('web_port',80).default('ws_address','127.0.0.1').default('ws_port',4000).argv

const wss = new WebSocket.Server({
    port: argv.ws_port
});

var read_data = []
// สร้าง websockets server ที่ port 4000
wss.on('connection', function connection(ws) { // สร้าง connection
    ws.on('message', function incoming(message) {
        // รอรับ data อะไรก็ตาม ที่มาจาก client แบบตลอดเวลา
        console.log('received: %s', message);
    });
    ws.on('close', function close() {
        // จะทำงานเมื่อปิด Connection ในตัวอย่างคือ ปิด Browser
        console.log('disconnected');
    });
    //ws.send('init message to client');
    // ส่ง data ไปที่ client เชื่อมกับ websocket server นี้

    setInterval(() => {
        //console.log('sending to data to client:', read_data)
        ws.send(JSON.stringify(read_data))
    }, 1000)
});

const express = require('express')
const app = express()
const web_port = argv.web_port

app.use(express.static('public'))

app.get('/', (req, res) => {
    res.sendFile('view/index.html', {
        root: __dirname
    })
})

app.listen(web_port, () => {
    console.log(`Example app listening at http://localhost:${web_port}`)
})

const ad_port = new serialport('/dev/ttyACM0', {
    baudRate: 115200
});
const parser = ad_port.pipe(new Readline({
    delimiter: '\r\n' 
}));

ad_port.on("open", () => {
    console.log('serial port open');
});

parser.on('data', data => {
    //console.log(data);
    try {
	read_data = JSON.parse(data);
    } catch (e) {}
    //console.log("read_data", read_data);
});
