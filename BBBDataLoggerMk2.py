import can
import mysql.connector as sql

#################################### SQL FUNCTIONS WE WILL NEED #########################################################
def connect(username,password,database):
    connect = sql.connect( user = username, password = password, database = database) # connected to database
    return connect
def cursor(connect):
    cursor = connect.cursor()
    return cursor
def add_message(data,cursor,connect):
    ###################################### Creating the Argument #######################
    add_message = "INSERT INTO can ( `msg_data` ) VALUES ('"
    add_message += data
    add_message += "')"
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

add_message("poop", cursor, connect)

can_interface = 'can0'
can_interface_type = 'socketcan_ctypes'

bus = can.interface.Bus(can_interface, can_interface_type)


while 1:
  message = bus.recv()
  
  
  
  # msg = can.Message(arbitration_id=0xc0ffee, data=[2, 0, 0, 1, 3, 1, 4, 1], extended_id=False)
  # bus.send(msg)
