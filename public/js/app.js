// ทำการเชื่อม Websocket Server ตาม url ที่กำหนด
var server_cube = [0,0,0];


function makeConnection(info) {

	var connection = new WebSocket('ws://'+info.address+':'+info.port)

	connection.onopen = function () {
	  // จะทำงานเมื่อเชื่อมต่อสำเร็จ
	  console.log("connect webSocket");
	  connection.send("Hello ABCDEF"); // ส่ง Data ไปที่ Server
	};
	connection.onerror = function (error) {
	  console.error('WebSocket Error ' + error);
	};
	connection.onmessage = function (e) {
	  // log ค่าที่ถูกส่งมาจาก server
	  console.log("message from server: ", e.data);
	  server_cube = JSON.parse(e.data)['ultra'];
	};

}

fetch('/ws_info').then(response => response.json()).then(data => makeConnection(data));
