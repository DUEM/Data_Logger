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
def add_message(msg_id, msg_data, cursor, connect):
    #time1 = datetime.datetime.now()
    ###################################### Creating the Argument #######################
    add_message = "INSERT INTO can ( 'msg_id', 'msg_data' ) VALUES ('"
    #add_message += str(time1)
    #add_message += ", "
    add_message += str(msg_id)
    add_message += "', "
    add_message += str(msg_data)
    add_message += ")"
    print(add_message)
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

msg = can.Message(arbitration_id=0x520, data=[2, 0, 0, 1, 3, 1, 4, 1], extended_id=False)
add_message(msg.arbitration_id, msg.data, cursor, connect)

"""
while 1:
  # add_message(str(bus.recv()), cursor, connect)
  
  msg = can.Message(arbitration_id=0xc0ffee, data=[2, 0, 0, 1, 3, 1, 4, 1], extended_id=False)
  print(msg.data);
  # bus.send(msg)
"""
