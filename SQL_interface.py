import mysql.connector as sql

connect = sql.connect(user = "python1", database = "test") # connected to database
cursor = connect.cursor()
add_message = ("INSERT INTO can ( `Time`, `Node ID`, `Node Type`, `Data` )VALUES (10,11,'sensor','hello world') ") 
cursor.execute(add_message) # updating the table
connect.
#this code doesnt work and im not sure why yet
