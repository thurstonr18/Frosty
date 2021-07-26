import requests
import json
import os
import glob
import time

# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_rom():
    name_file = device_folder + '/name'
    f = open(name_file, 'r')
    return f.readline()


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def form_request(temp):
    url = 'http://192.168.1.128:8000/post_temp/'

    client = requests.session()

    client.get(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.102 Safari/537.36 '
    }
    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    else:
        # older versions
        csrftoken = client.cookies['csrf']

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'temp': temp,

    }

    
    r1 = client.get(url, data=login_data, headers=headers)
    r2 = client.post(url, data=payload, headers=headers, timeout=3.5)

    time.sleep(10)
    form_request(read_temp())

time.sleep(10)
form_request(read_temp())
