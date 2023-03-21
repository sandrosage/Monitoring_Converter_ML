import numpy as np 
import time 
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import socket
import select
import threading
import re
import RPi.GPIO as GPIO
from time import sleep
import serial
from playsound import playsound
import os
import struct
import smbus

old_temp = 0
run_data = ''
i2c_ch = 1
i2c_address = 0x48
reg_temp = 0x00
reg_config = 0x01


ip_nn = '10.60.2.41'
port3 = 8997

filename = ''

data_to_send = []
ser = serial.Serial("/dev/ttyACM0", 115200)
ser.reset_input_buffer()

def calc_i_out(high, low):
    val = (int.from_bytes(high, "little") << 8)+ int.from_bytes(low, "little")
    Amps = (val/1024*5)/0.3
    return Amps

def calc_temp(high, low):
    val = (int.from_bytes(high, "little") << 8) + int.from_bytes(low, "little")
    Temp = ((val /1024 * 5) -0.4) / 0.0195
    return Temp

def calc_v_out(high, low):
    val = (int.from_bytes(high, "little") << 8) + int.from_bytes(low, "little")
    Volt = (val /1024 * 5) * 6
    return Volt

    
def calc_v_in(high, low):
    val = (int.from_bytes(high, "little") << 8) + int.from_bytes(low, "little")
    Volt = (val /1024 * 5) * 13
    return Volt

    
def split_data(data_list):
  delimiters = '.fn'
  regexPattern = '|'.join(map(re.escape, delimiters))
  pf = re.findall(regexPattern, data_list)
  y = re.split(regexPattern, data_list)
  return y,pf


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def read_temp():
    global bus
    global val
    try:
        val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    except:
        print("Exception\n")
        bus.close()
        time.sleep(0.1)
        bus = smbus.SMBus(i2c_ch)
        print("Bus resetted")
    temp_c = (val[0] << 4) | (val[1] >> 5)
    temp_c = twos_comp(temp_c, 12)
    temp_c = temp_c * 0.0625
    return temp_c

def ssock(x):
    print("Running")
    c, addr = s.accept()
    time.sleep(0.5)
    x = c.recv(1024)
    print("RECEIVED")
    global run_data
    global filename
    y, pf = split_data(x.decode("utf-8"))
   
    print(x.decode("utf-8"))
    if(x.decode("utf-8") == '1'):
        run_data = "Run"
        print("Starting Recording")
        print("Enterd Run")
    elif(x.decode("utf-8") == '2'):
        run_data = ''
        print("Stopping recording")
    elif(x.decode("utf-8") == '3'):
        f = open(filename+'.txt', 'rb')
        l = f.read(1024)
        while(l):
          c.send(l)
          l = f.read(1024)
        print("Data send")
    elif(x.decode("utf-8") == '4'):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, GPIO.LOW)
        print("Killing Power")
    elif(x.decode("utf-8") == '-2'):
        print("Quitting Programm")
        run_data = 'Quit'
    else:
        print(y[0])
        filename = y[0]
        
def write_file(x):
    global old_temp
    global data_to_send
    val_list = []
    #Für Client server: "run_data == "Run"" einfügen, für normalen betrieb while(1)
    while(1):
        response = ser.read()
        if(response != b"V" and response != b"I" and response != b"O" and response != b"T"):
            val_list.append(response)

        if(response == b'V'):
            while(len(val_list) < 2):
                val_list.append(b'0')
            x = calc_v_in(val_list[0], val_list[1])
            data_to_send.append(x)
            val_list = []


        if(response == b'I'):
            while(len(val_list) < 2):
                val_list.append(b'0')
            x = calc_i_out(val_list[0], val_list[1])
            print("Strom: ", x)
            data_to_send.append(x)
            val_list = []
            


        if(response == b'O'):
            while(len(val_list) < 2):
                val_list.append(b'0')
            x = calc_v_out(val_list[0], val_list[1])
            print("VOUT: ", x)
            data_to_send.append(x)
            val_list = []


        if(response == b'T'):
            while(len(val_list) < 2):
                val_list.append(b'0')
            x = calc_temp(val_list[0], val_list[1])
            print("Temperatur:", x)
            if(x < 0):
                x = x + 63.601
            data_to_send.append(x)
            temperature = read_temp()
            data_to_send.append(temperature)
            #Dateinamen hier umstellen
            with open("STAT_DROSSEL_6A.txt", "a") as t:
                t.write(str(data_to_send)+"\n")
            data_to_send = []
            val_list = []
  


port = 8998

try:
    s = socket.socket()
    print("Socket Init")
except socket.error as err:
    print("Socket not Init")


s.bind(('', port))
print("Socket binded to", port)
s.listen()

bus = smbus.SMBus(i2c_ch)
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("Old CONFIG:", val)
val[1] = val[1] & 0b00111111
val[1] = val[1] | (0b10 << 6)
bus.write_i2c_block_data(i2c_address, reg_config, val)
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)


while(1):
    y = threading.Thread(target = ssock, args = (1,))
    y2 = threading.Thread(target = write_file, args =(1,))

    y.start()
    y2.start()
    if(run_data == "Quit"):
        s.close()
        bus.close()
        sys.exit()
        y.join()
        y2.join()
        
    y.join()
    y2.join()

