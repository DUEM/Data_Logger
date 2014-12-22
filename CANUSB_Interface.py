
import serial
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
ser = serial.Serial()
ser.port = "COM7"
ser.baudrate = 115200
ser.timeout = 1
ser.open()
if(ser.isOpen()):
    print("Port opened")
    ser.write(b"\r\r\r") #Clear residual messages 
    ser.write(b"S6\r") #Set canusb speed of 500kbit/s
    ser.write(b"O\r") #Open canusb
    print(ser.read(5))
    print("CANUSB activated")

else:
    print( "Port did not open")

#Sort messages
t=0
while t<100: #arbitrary number to ensure port eventually closes
    print("No. " +str(t))
    x= ser.read(22)
    y=list(x)
    if x != "":
        joined = "0x"+y[1]+y[2]+y[3]
        node_id = int(joined,0)
        data=""
        for j in range(5,21,1):
            data+=y[j]
        data=data.decode("hex")
         ######### SQL BIT HERE ########################################
        connect = connect("InsertUserNameHere","InsertTableNameHere")
        cursor = cursor(connect)
        add_message(str(node_id),str(data),cursor,connect)
        ###############################################################
        print("Node "+ str(node_id) + " message:"+"\n"+data+"\n")
        t+=1
    else:
        t+=1
        print("No message")
    #close port when finished
ser.write(b"C\r") #Close CANUSB
ser.close()

