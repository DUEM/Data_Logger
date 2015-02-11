import mysql.connector as sql
import time   

def connect(username,password,database):
    connect = sql.connect(user = username,password=password, database = database) # connected to database
    return connect
def cursor(connect):
    cursor = connect.cursor()
    return cursor
def add_message(node_id,data,cursor,connect):
    time1 = str(0)

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
    
    #################################### Creating the Argument #########################
    query_message = "SELECT `Node ID`,`Time`, `Data` FROM can WHERE "
    filterItem = str(input("ENTER FILTER TERM HERE: "))
    query_message += "`"
    query_message += filterItem
    query_message += "` BETWEEN "
    LowfiltRange =  str(input("ENTER LOWER LIMIT HERE: "))
    HighfiltRange =  str(input("ENTER UPPER LIMIT HERE: "))
    query_message += LowfiltRange
    query_message += " AND "
    query_message += LowfiltRange
    print(query_message)
    arg = ("SELECT `Node ID`,`Time`, `Data` FROM can WHERE `Node ID` BETWEEN 0 AND 1000")
    # make query editable
    cursor.execute(query_message)
    return cursor
    
username = str(input("Enter Username: "))
database = str(input("Enter Database: "))
password = str(input("Enter Password: "))
connect = connect(username,password,database)
cursor = cursor(connect)
