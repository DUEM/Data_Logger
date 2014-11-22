import mysql.connector as sql

connect = sql.connect(user = "python1", database = "test") # connected to database
cursor = connect.cursor()
add_message = ("INSERT INTO can " 
               "( Time, Node ID, Node Type, Data )"
               "VALUES (%s,%s,%s,%s) ") 
message_data = ()#place data in here
cursor.execute(add_message,message_data) # updating the table
#this code doesnt work and im not sure why yet
