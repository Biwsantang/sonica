import scipy.io as sio
import paho.mqtt.client as mqtt
import ujson
import numpy as np

host = "124.121.139.47"
port = 1883

ranges_mat = []
scanAngles_mat = [0,0.5235987756,1.0471975512,1.5707963268,2.0943951024,2.6179938780,3.1415926536]
pose_mat = []
t_mat = []

def saveToArr(raw):
    data = ujson.loads(raw)
    pose_mat.append([data["X"],data["Y"],data["theta"]])
    ranges_mat.append([data["US_L1"],
                       data["US_L2"],
                       data["US_L3"],
                       data["US_C"],
                       data["US_R3"],
                       data["US_R2"],
                       data["US_R1"]])
    t_mat.append(data["T"])
    saveToMat()

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("esp/test")

def on_message(client, userdata, msg):
    raw = msg.payload.decode("utf-8", "strict")
    print(raw)
    saveToArr(raw)

def saveToMat():
    print("=============SAVE==========")
    sio.savemat("62_real_robot.mat", {
        'init_pose': np.array(pose_mat[0]).reshape(-1, 1),  # initial_position
        'pose': np.array(pose_mat).T,  # current_position
        'ranges': np.array(ranges_mat).T,  # Ultrasonics_range_data
        'scanAngles': np.array(scanAngles_mat).reshape(-1, 1),  # Ultrasonics_angle
        't': np.array(t_mat).T  # Timestamp
    })

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    client.loop_forever()

if __name__ == "__main__":
    run()

