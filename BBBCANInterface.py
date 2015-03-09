import socket
import struct
import serial
import sys
import mysql.connector as sql
import datetime
import random

#################################### SQL FUNCTIONS WE WILL NEED #########################################################
def connect(username,password,database):
    connect = sql.connect( user = username,password=password, database = database) # connected to database
    return connect
def cursor(connect):
    cursor = connect.cursor()
    return cursor
def add_message(node_id,data,cursor,connect):
    time1 = datetime.datetime.now()
    print(time1)
    ###################################### Creating the Argument #######################
    add_message = "INSERT INTO can ( `Time`, `Node ID`, `Data` )VALUES ('"
    add_message += str(time1)
    add_message += "','"
    add_message += node_id
    add_message += "','"
    add_message += data
    add_message += "')"
    print(add_message)
    cursor.execute(add_message)
    connect.commit()
    return 1
def query(cursor,connect):
    arg = ("SELECT `Node ID`,`Time`, `Data` FROM can WHERE `Node ID` BETWEEN 0 AND 1000")
    # make query editable
    cursor.execute(arg)
    return cursor
#########################################################################################################################

can_frame_fmt = "=IB3x8s"
can_frame_size = struct.calcsize(can_frame_fmt)

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return (can_id, can_dlc, data[:can_dlc])

def check_input(file,ser=0):
    input = file.read(4)
    if input == "":
        print("No input")
    else:
        input_array=list(input)
        message_bytes=file.read(2*int(input_array[3]))
        file.seek(file.tell()+2)
        a=""
        for x in message_bytes:
            a +=x
        try:
            s.send(build_can_frame(int(input_array[3]), bytes(a,'utf-8')))
        except OSError:
            print('Error sending CAN frame')
            
            
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(('can0',))
username="ed"
database="test"
password="runrun93"
connect = connect(username,password,database)
cursor = cursor(connect)
sync = open("CAN_TimeSync.canusb","r")
line = sync.readline()
print(line)
file = open(line,"r")
while 1:
    check_input(file)
    cf, addr = s.recvfrom(can_frame_size)
    can_id, can_dlc, data = dissect_can_frame(cf)
    print('Received: can_id=%x, can_dlc=%x, data=%s' % can_id, can_dlc, data)
    add_message(can_id,data,cursor,connect)
