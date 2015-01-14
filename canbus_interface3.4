
import SQL_interface
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
    x = ser.read(5)




#Sort messages
def sort_messages(ser,t):
    print("No. " +str(t))
    x= ser.read(22)
    print(x)
    y=list(x)
    if x != b"":
        node_id = chr(y[1])+chr(y[2])+chr(y[3])
        data=""
        for j in range(5,21,1):
            data = data + chr(y[j])
        print("Node "+node_id+ " message:"+"\n"+data+"\n")
        return (node_id,data)
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
        print(input)
        close_canusb(ser)
        file.seek(file.tell()+2)
    elif input=="OPENCBUS":
        print(input)
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
        print(input)
        to_send = "t0008"+input+"\r"
        ser.write(b"t000812345678\r")
        x=ser.read(2)
        while x != "z\r":
            ser.write(b"t000812345678\r")
            x=ser.read(2)
            print(x)
            print("Message not sent!")
        print("Message Sent")
    return ser

#Start of program
global CANOPEN
CANOPEN = 0
t=0
ser = 0
connect = connect("InsertUserNameHere","InsertTableNameHere")
cursor = cursor(connect)
file = open(r"C:\Users\Ed\Desktop\CAN_Input.canusb","r")
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



