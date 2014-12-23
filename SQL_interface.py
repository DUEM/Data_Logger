import mysql.connector as sql
import time   

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
    
username = str(input("Enter Username: "))
database = str(input("Enter Database: "))
connect = connect(username,database)
cursor = cursor(connect)
while 1==1:
    print("1) Adding Data to Table")
    print("2) Query Table")
    choice = str(input("Choose Option: "))
    if choice == str(1):
        node_id = str(input("Enter Node ID: "))
        data = str(input("Enter Data: "))
        add_message(node_id,data,cursor,connect)

    if choice == str(2):
        cursor = query(cursor,connect)
        for (item) in cursor:
            print(item) # v.basic printing needs improving!!!
