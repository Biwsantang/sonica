const char MAIN_page[] PROGMEM = R"=====(
<!DOCTYPE html>
<html>
  <head>
    <script>
      function stop() {
        fetch('/stop'); 
      }
      function reset() {
        fetch('/reset');
      }
      function move(steps_direction) {
        var speedL = document.getElementById("speedL").value;
        var speedR = document.getElementById("speedR").value;
        
        fetch('/move?steps_direction='+steps_direction+'&speedL='+speedL+'&speedR='+speedR);
      }
    </script>
  </head>
  <body>
    <label for="speedL">Speed Left Motor</label>
    <input type="text" id="speedL"></input><br><br>
    <label for="speedR">Speed Right Motor</label>
    <input type="text" id="speedR"></input><br><br>
    
    <button id="Forward" type="button" onmousedown="move(3)" onmouseup="stop()">Forward</button><br><br>
    <button id="Backward" type="button" onmousedown="move(2)" onmouseup="stop()">Backward</button><br><br>
    <button id="Left" type="button" onmousedown="move(1)" onmouseup="stop()">Left</button><br><br>
    <button id="Right" type="button" onmousedown="move(4)" onmouseup="stop()">Right</button><br><br>
    <button id="Stop" type="button" onclick="stop()">Stop</button><br><br>
    <button id="Reset" type="button" onclick="reset()">Reset</button><br><br>
  </body>
</html>
)=====";
