// ทำการเชื่อม Websocket Server ตาม url ที่กำหนด
var server_cube = [0,0,0];


function makeConnection(info) {

	var ws = new WebSocket('ws://'+info.address+':'+info.port)

	ws.onopen = function () {
	  // จะทำงานเมื่อเชื่อมต่อสำเร็จ
	  console.log("connect webSocket");
	  ws.send("Open Connection"); // ส่ง Data ไปที่ Server
	}
	ws.onerror = function (error) {
	  console.error('WebSocket Error ' + error);
	};
	ws.onmessage = function (e) {
	  // log ค่าที่ถูกส่งมาจาก server
	  console.log("message from server: ", e.data);
	  server_cube = JSON.parse(e.data)['ultra'];
	};

}

fetch('/ws_info').then(response => response.json()).then(data => makeConnection(data));
