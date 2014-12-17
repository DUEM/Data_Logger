import mysql.connector as sql

connect = sql.connect(user = "python1", database = "test") # connected to database
cursor = connect.cursor()
add_message = ("INSERT INTO can ( `Time`, `Node ID`, `Node Type`, `Data` )VALUES (10,11,'sensor','hello world') ") 
cursor.execute(add_message) # updating the table
connect.commit()
#this code doesnt work and im not sure why yet

######################### querying a table ####################################################
query = ("SELECT `Node ID`,`Node Type`, `Data` FROM can WHERE `Node ID` BETWEEN 1 AND 3")
# choose which columns you want outputted          "SELECT `Node ID`,`Node Type`, `Data` FROM can"
# choose how you wish to filter with               "WHERE `Node ID` BETWEEN 1 AND 3"
cursor.execute(query)

for (item) in cursor:
  print(item) # v.basic printing
    
#Need to make the values within the command editable (use string conc.)
