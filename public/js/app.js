// ทำการเชื่อม Websocket Server ตาม url ที่กำหนด
var server_cube = [0,0,0];
var rotate = [0,0,0];
var s_rotate
var p_rotate
var first = 1;


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
	  //console.log("message from server: ", e.data);
		data = JSON.parse(e.data)
	  server_cube = [data[0],data[1],data[2]];
		rotate =  [data[3],data[4],data[5]];
		if(first){
			first = 0;
			s_rotate = rotate;
			p_rotate = rotate;
		}
	};

}

fetch('/ws_info').then(response => response.json()).then(data => makeConnection(data));
