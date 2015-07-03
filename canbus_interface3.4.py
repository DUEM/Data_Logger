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

#open port
def open_ports(file):
    inputed=file.read(12)
    inputed =inputed.strip("")
    while inputed =="":
        inputed=file.read(12)
        print("enter port")
    port =inputed.strip("")
    print(port)
    file.seek(file.tell()+2)
    inputed=file.read(6)
    while inputed =="":
        inputed=file.read(6)
        print("enter rate")
    baudrate = int(inputed.strip(""))
    print(baudrate)
    try:
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = baudrate
        ser.timeout = 1
        ser.open()
        if(ser.isOpen()):
            print("Port opened")
        else:
            print( "Port did not open")
        return ser
    except serial.SerialException:
        print("CANBUS disconnected")
#Activate Canbus
def open_canbus(ser):
    global CANOPEN
    CANOPEN=1
    try:
        ser.write(b"\r\r\r") #Clear residual messages
        ser.write(b"S6\r") #Set canusb speed of 500kbit/s
        ser.write(b"O\r") #Open canusb
        print("CANUSB activated")
        x = ser.read(5)
        print(x)
    except serial.SerialException:
        print("CANBUS disconnected")

#Sort messages
def sort_messages(ser,t):
    print("No. " +str(t))
    try:
        start_message= ser.read(1)
        if  start_message.decode('utf-8') == "t":
            node_id_bytes= ser.read(3)
            node_array=list(node_id_bytes)
            node_id = chr(node_array[0])+chr(node_array[1])+chr(node_array[2])
            length= ser.read(1)
            length.decode('utf-8')
            length=int(length)*2
            message_bytes= ser.read(length)
            message_array=list(message_bytes)
            message=""
            for j in range(0,length,1):
                message += chr(message_array[j])
            print("Node "+node_id+ " message:"+"\n"+message+"\n")
            end_message = ser.read(1)
            if end_message != "\r":
                #do something else
                a=1
            #message=str(int(message,16))

            return (node_id,message)
        else:
            print("No message")
            return (0,0)
    except serial.SerialException:
        print("CANBUS disconnected")

#close port when finished
def close_canusb(ser):
    try:
        ser.write(b"C\r") #Close CANUSB
        ser.read(1)
        global CANOPEN
        CANOPEN=0
    except serial.SerialException:
        print("CANBUS disconnected")

def close_serial(ser):
    close_canusb(ser)
    ser.close()
    global CANOPEN
    CANOPEN = 2

def check_input(file,ser=0):
    input = file.read(4)

    print("Message to send:")
    if input == "":
        print("No message sent")
    else:
        input_array=list(input)
        message_bytes=file.read(2*int(input_array[3]))
        file.seek(file.tell()+2)
        a=""
        print("Input is " + input+message_bytes)
        joined=input+message_bytes
        for x in joined:
            a +=x
        try:
            print("t"+a+"\r")
            ser.write(b"t"+bytes(a,'utf-8')+b"\r")
            x=ser.read(2)
            while x != b"z\r":
                print("Message not sent!")
                ser.write(b"t1118"+bytes(a,'utf-8')+b"\r")
                x=ser.read(2)
            print("Message Sent")
        except serial.SerialException:
            print("CANBUS disconnected")
    return ser

#Start of program
global CANOPEN
CANOPEN = 0
t=0
#username = str(input("Enter Username: "))
username="ed"
#database = str(input("Enter Database: "))
database="test"
#password = str(input("Enter Password: "))
password="password"
connect = connect(username,password,database)
cursor = cursor(connect)

config = open("CAN_Config2.canusb","r")
ser=0
ser = open_ports(config)
open_canbus(ser)
sync = open("CAN_TimeSync.canusb","r")
line = sync.readline()
print(line)
file = open(line,"r")

while 1:
    ser =check_input(file,ser)
    if CANOPEN==1:
        message=sort_messages(ser,t)
        if message[1]!=0:
            add_message(message[0],message[1],cursor,connect)
        t=t+1
    elif CANOPEN == 2:
        print("Serial Port Closed")
    else:
        print("CAN Closed")



