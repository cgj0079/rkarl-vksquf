from flask import Flask, jsonify
import os, glob, time

app = Flask(__name__)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]  # 28로 시작하는 디렉토리
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c, 1)
    return None

@app.route("/temp")
def get_temp():
    temp = read_temp()
    return jsonify({"temperature": temp})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
