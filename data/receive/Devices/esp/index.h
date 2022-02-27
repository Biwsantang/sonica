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
      function move() {
        var steps_direction = document.getElementById("steps_direction").value;
        var stepsL = document.getElementById("stepsL").value;
        var stepsR = document.getElementById("stepsR").value;
        var speedL = document.getElementById("speedL").value;
        var speedR = document.getElementById("speedR").value;
        
        fetch('/move?steps_direction='+steps_direction+'&stepsL='+stepsL+'&stepsR='+stepsR+'&speedL='+speedL+'&speedR='+speedR);
      }
    </script>
  </head>
  <body>
    <label for="steps_direction">Steps Direction</label>
    <input type="text" id="steps_direction"></input><br><br>
    <label for="steps">Steps Left Motor</label>
    <input type="text" id="stepsL"></input><br><br>
    <label for="steps">Steps Right Motor</label>
    <input type="text" id="stepsR"></input><br><br>
    <label for="speedL">Speed Left Motor</label>
    <input type="text" id="speedL"></input><br><br>
    <label for="speedR">Speed Right Motor</label>
    <input type="text" id="speedR"></input><br><br>
    
    <button id="Forward" type="button" onclick="move()">Forward</button><br><br>
    <button id="Stop" type="button" onclick="stop()">Stop</button><br><br>
    <button id="Reset" type="button" onclick="reset()">Reset</button><br><br>
  </body>
</html>
)=====";
