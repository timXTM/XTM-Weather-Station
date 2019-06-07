import glob
import sys
import time
import datetime
import json
from influxdb import InfluxDBClient

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'temp')


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_tempC():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def read_tempF():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f
try:
    while True:
        now = time.ctime()
        celcius_temp = read_tempC()
        print(read_tempC(), 'C, ')
        with open("temp_data.json", "w") as write_file:
            json.dump(read_tempC(), write_file)
        json_body = [{
            "measurement": "Celcius",
                "tags": {
                    "location": "weather-station",
                },
            "fields": {
                "temperature" : celcius_temp,
            }
        }]

        dbClient.write_points(json_body)
        time.sleep(1)

except KeyboardInterrupt:
    pass

