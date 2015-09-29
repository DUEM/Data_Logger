import can
import mysql.connector as sql
import datetime

#################################### SQL FUNCTIONS WE WILL NEED #########################################################
def connect(username,password,database):
    connect = sql.connect( user = username, password = password, database = database) # connected to database
    return connect
def cursor(connect):
    cursor = connect.cursor()
    return cursor
def add_message(msg_id, msg_len, msg_data, cursor, connect):
    time1 = datetime.datetime.now()
    ###################################### Creating the Argument #######################
    add_message = "INSERT INTO can ( msg_time, msg_id, msg_len, msg_data ) VALUES ('"
    add_message += str(time1)
    add_message += "', '"
    add_message += str(msg_id)
    add_message += "', '"
    add_message += str(msg_len)
    add_message += "', "
    data_string = ""
    if msg_data:
        data_string = ""
        for byte in msg_data:
            data_string = "".join( ( "%.2x" % byte, data_string) )
        data_string = "0x" + data_string
    add_message += data_string
    add_message += " )"
    #print(add_message)
    cursor.execute(add_message)
    connect.commit()
    return 1
#########################################################################################################################

username="root"
database="test"
password="dusc2015"
connect = connect(username,password,database)
cursor = cursor(connect)
# CREATE TABLE can( msg_no BIGINT AUTO_INCREMENT PRIMARY KEY, msg_time DATETIME, msg_id INT, msg_data VARBINARY(8));

can_interface = 'can0'
can_interface_type = 'socketcan_ctypes'

bus = can.interface.Bus(can_interface, can_interface_type)

#msg = can.Message(arbitration_id=0x520, data=[2, 0, 0, 1], extended_id=False)
#add_message(msg.arbitration_id, msg.data, cursor, connect)


while 1:
    msg = bus.recv()
    add_message(msg.arbitration_id, msg.dlc, msg.data, cursor, connect)
  
  # bus.send(msg)

