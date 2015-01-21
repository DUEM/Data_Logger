#!/usr/bin/env python3
import SQL_Interface
import serial
import sys

import mysql.connector as sql
import time
#################################### SQL FUNCTIONS WE WILL NEED #########################################################
def connect(username,database):
    connect = sql.connect(user = username, database = database) # connected to database
    return connect
def cursor(connect):
    cursor = connect.cursor()
    return cursor
def add_message(node_id,data,cursor,connect):
    time1 = time.strftime('%Y-%m-%d %H:%M:%S')

    ###################################### Creating the Argument #######################
    add_message = "INSERT INTO can ( `Time`, `Node ID`, `Data` )VALUES ('"
    add_message += time1
    add_message += "','"
    add_message += node_id
    add_message += "','"
    add_message += data
    add_message += "')"
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
    port =(file.read(8)).strip("")
    print(port)
    file.seek(file.tell()+2)
    baudrate = int((file.read(8)).strip(""))
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
#Activate Canbus
def open_canbus(ser):
    global CANOPEN
    CANOPEN=1
    ser.write(b"\r\r\r") #Clear residual messages
    ser.write(b"S6\r") #Set canusb speed of 500kbit/s
    ser.write(b"O\r") #Open canusb
    #print("CANUSB activated")
    ser.read(5)


#Sort messages
def sort_messages(ser,t):
    print("No. " +str(t))
    x= ser.read(22)
    y=list(x)
    if x != "":
        joined = "0x"+y[1]+y[2]+y[3]
        node_id = int(joined,0)
        data=""
        for j in range(5,21,1):
            data = data + ("0"+((hex(ord(y[j])))[2:]))[-2:]
        print(data.decode("hex"))
        return(str(node_id),str(data))
        print("Node "+ str(node_id) + " message:"+"\n"+data.decode("hex")+"\n")
    else:
        print("No message")
        return 42

#close port when finished
def close_canusb(ser):
    ser.write(b"C\r") #Close CANUSB
    ser.read(1)
    global CANOPEN
    CANOPEN=0

def close_serial(ser):
    close_canusb(ser)
    ser.close()
    global CANOPEN
    CANOPEN = 2

def check_input(file,ser=0):
    input = file.read(8)
    print("Message to send:")
    if input == "":
        print("No message sent")
    elif input=="CLOSEBUS":
        a=""
        for x in input:
            a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
        print(a.decode("hex"))
        close_canusb(ser)
        file.seek(file.tell()+2)
    elif input=="OPENCBUS":
        a=""
        for x in input:
            a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
        print(a.decode("hex"))
        open_canbus(ser)
        file.seek(file.tell()+2)
    elif input=="CLOSESER":
        close_serial(ser)
        file.seek(file.tell()+2)
    elif input =="OPENSERL":
        file.seek(file.tell()+2)
        ser = open_ports(file)
        file.seek(file.tell()+2)
    elif input == "EXITPROG":
        if CANOPEN == 2:
            print("Program exited")
            sys.exit()
        else:
            close_canusb(ser)
            file.seek(file.tell()+2)
            close_serial(ser)
            file.seek(file.tell()+2)
            print("Program exited")
            sys.exit()

    else:
        file.seek(file.tell()+2)
        a=""
        for x in input:
            a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
        print(a.decode("hex"))
        ser.write(b"t1118"+a+"\r")
        print("t1118"+a+"\r")
        x=ser.read(2)
        if x == "z\r":
            print("Message Sent\n")
        else:
            print("Message not sent!\n")
    return ser

#Start of program
global CANOPEN
CANOPEN = 0
t=0
ser = 0
connect = connect("InsertUserNameHere","InsertTableNameHere")
cursor = cursor(connect)
file = open("C:\Users\Ed\Desktop\CAN_Input.canusb","r")
while 1:
    ser =check_input(file,ser)
    if CANOPEN==1:
        message=sort_messages(ser,t)
        add_message(message[0],message[1],cursor,connect)
        t=t+1
    elif CANOPEN == 2:
        print("Serial Port Closed")
    else:
        print("CAN Closed")



