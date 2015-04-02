#!/usr/bin/env python3
import socket, sys, threading, struct #, socketserver
import random
import datetime
#import SQL_interface
from queue import Queue
## SERVER

q1 = Queue() # talk to recieve CAN thread
q1.join()

q2 = Queue() #Talk to Send CAN thread
q2.join()

def threadFunc(conn, addr):
    while 1:
        #connect = SQL_interface.connect(SQL_interface.username,SQL_interface.password,SQL_interface.database)
        #cursor = SQL_interface.cursor(connect)
        try: #getting message
            message1 = conn.recv(2048)
            if not len(message1):
                print("Disconnected with " + addr[0] + ":" + str(addr[1]))
                conn.close()
                break
            if type(message1) == bytes:
                message1 = message1.decode("utf-8")
                print("Received: " + str(message1))
            else:
                print("Received: " + str(message1))
        except:
            print("Failed to recieve the message")
            conn.close()
            break
        if message1 == "_db_":
            if addr[0] == "127.0.0.1":
                global db_clients_INFO
                info = get_info(db_clients_INFO)
                msg1 = (str(info)).encode("utf-8")
            else:
                info = "You don\'t have permission to access this database\n"
                msg1 = (str(info)).encode("utf-8")
        elif message1 == "_info_":
            info = "1) _db_ for users info database\n"
            info += "2) _mv_ for movies database\n"
            msg1 = (str(info)).encode("utf-8")
#############################################################################################################################
#******************************************** Sensor Data Request **********************************************************#
#############################################################################################################################
        elif message1 == "Speed_data":
            #get speed data here (query sql database or get it live of the CAN)
            #Query SQL
            
            ##########
            info = "Speed_data: "
            info += str(speed_data)
            msg1 = (str(info)).encode("utf-8")
        elif message1 == "Temp_data_all":
            #get temp data from all sources here (query sql database or get it live of the CAN)
            #query SQL
            
            
            ##########
            info = "Temp data" + str(source_id) + ": " #get the id of the node which sent the data
            info += str(temp_data)
            msg1 = (str(info)).encode("utf-8")
        elif message1 == "Bat_SOC":
            #get SOC data (query sql database or get it live of the CAN) 
            #going to query SQL
            
            
            ###################
            info = "SOC: " 
            info += str(SOC)
            msg1 = (str(info)).encode("utf-8")
############################################################################################################################
#******************************************************** Recieving Commands **********************************************#
############################################################################################################################
        elif "_SEND_CAN_MESSAGE_" in message1:
            # checks if want to send a can message 
            #send message to other programme here
             #some method to send a can message
            #file = open(filename,"a") #file path will need changing
            #file.write(message1.replace("_SEND_CAN_MESSAGE_","")+"\r\r")
            #file.close()
            message1 = message1.replace("_SEND_CAN_MESSAGE_","")
            print("sending Can Message: " + message1)
            print(message1)
            q2.put(message1)
            msg1 = (str(message1)).encode("utf-8")
            ##################################### 
        elif "_SET_MESSAGE_FREQUENCY_" in message1:
            # checks if want to change the rate a messages are sent at 
            msg_freq = message1[-1] # set the frequency of messages
        elif "_SET_SAVE_FREQUENCY_" in message1:
            # checks if want to change how often to save on the loggers local storage
            save_freq = message1[-1] #set message save frequency
        elif "_STOP_RECORDING_CAN_" in message1:
            #send command to other programme here
            print("stop")
            ####################################
        elif "_MONITOR_CAN_BUS_" == message1:
            # get live can bus activity and send to client
            # probs create a thread to wait for activity and send to the client
            #message1 = "Displaying Live CAN Activity"
            #last_message_time="2015-02-04 16:20:26.558000"
            last_message_time = "401"
            #a_long_time="2020-02-04 16:20:26.558000"
            a_long_time="499"
            latest_message = SQL_interface.query(cursor,connect,"Node ID",last_message_time,a_long_time)
            for (Time, Node_ID, Data) in latest_message:
                message1 = "_MONITOR_CAN_BUS_"+"{1}, {0} {2}".format(Time, Node_ID, Data)
                print(message1)
                msg1 = (str(message1)).encode("utf-8")
        elif "_STOP_MONITOR_CAN_BUS_" == message1:
            #stops sending live CAN data
            message1 = "No Longer Displaying Live CAN Activity"
            msg1 = (str(message1)).encode("utf-8")
        elif "_COM_LIVE_PLOT_BAT_" in message1:
            message1 = "_COM_LIVE_PLOT_BAT_" + str(random.randrange(1,10+1))
            msg1 = (str(message1)).encode("utf-8")
        elif "_COM_SAVE_BAT_" in message1:
            message1 = "_COM_SAVE_BAT_" + str(random.randrange(1,10+1))
            msg1 = (str(message1)).encode("utf-8")
        elif "_COM_LIVE_PLOT_SPEED_" in message1:
            message1 = "_COM_LIVE_PLOT_SPEED_" + str(random.randrange(1,10+1))
            msg1 = (str(message1)).encode("utf-8")
        elif "_COM_SAVE_SPEED_" in message1:
            message1 = "_COM_SAVE_SPEED_" + str(random.randrange(1,10+1))
            msg1 = (str(message1)).encode("utf-8")
        elif "_COM_LIVE_PLOT_TEMP_" in message1:
            message1 = "_COM_LIVE_PLOT_TEMP_" + str(random.randrange(1,10+1))
            msg1 = (str(message1)).encode("utf-8")
        elif "_COM_SAVE_TEMP_" in message1:
            message1 = "_COM_SAVE_TEMP_" + str(random.randrange(1,10+1))
            msg1 = (str(message1)).encode("utf-8")
#############################################################################################################################
#******************************************************** Errors ***********************************************************#
#############################################################################################################################
        else:
            message1 = "Unknown command \nType: _info_ for a list of commands"
            msg1 = (str(message1)).encode("utf-8")
#############################################################################################################################
#**************************************************** Sending Message ******************************************************#
#############################################################################################################################
        try:
            conn.sendall(msg1)
        except:
            print("Failed to send the message")


def con_info(addr):
    host,port = addr
    try:
        results = socket.getaddrinfo(host,port,0,socket.SOCK_STREAM)
    except:
        results = []
        print("[Error] cannot get info about the client")
    return results

def get_info(db):
    info = ""
    for results in db:
        for result in results:
            info += ("_"*40)
            info += "\n"
            if result[0] == socket.AF_INET:
                info += ("Family: AF_INET")
            elif result[0] == socket.AF_INET6:
                info += ("Family: AF_INET6")
            else:
                info += ("Family:",result[0])
            info += "\n"
            if result[1] == socket.SOCK_STREAM:
                info += ("Socket Type: SOCK_STREAM")
            elif result[1] == socket.SOCK_DGRAM:
                info += ("Socket Type: SOCK_DGRAM")
            else:
                info += ("Unknown type:",result[1])
            info += "\n"
            info += ("Protocol: "+str(result[2]))
            info += "\n"
            info += ("Canonical Name: "+str(result[3]))
            info += "\n"
            info += ("Socket Address: "+", ".join([str(x) for x in result[4]]))
            info += "\n"
            info += ("_"*40)
            info += "\n"
    return info

def main():
    global db_clients_INFO
    global db_clients_IP
    host = ''
    port = 51432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(5)
    print("Starting server")
    CanInt() # Start CAN Stuff
    while 1:
        conn, addr = s.accept()
        c = con_info(addr)
        if c[0][4][0] not in db_clients_IP:
            db_clients_IP.append(c[0][4][0])
            db_clients_INFO.append(c)
        t = threading.Thread(target = threadFunc, args = (conn, addr))
        print("Connected with: " + addr[0] + ":" + str(addr[1]))
        t.start()
    s.close()

#################################################################
###################### CAN STUFF ################################
#################################################################
def CanInt(): # Initialises all the CAN stuff
	can_frame_fmt = "=IB3x8s"
	can_frame_size = struct.calcsize(can_frame_fmt)
	cansock = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
	cansock.bind(('can0',))
	# clears the que before it is used

	
	CANListen = threading.Thread(target = lambda: recieveCanMessage(can_frame_size, can_frame_fmt, cansock))
	CANListen.daemon = True
	CANListen.start()
	while q2.empty() == False:            
		q2.get()
		q2.task_done()
		#starting CAN send thread
	
	CANTalk = threading.Thread(target = lambda: SendCanMessage(can_frame_fmt, 0x400,cansock))
	#example of how you communicate with the send thread
	CANTalk.daemon = True
	CANTalk.start()

	
def recieveCanMessage(can_frame_size, can_frame_fmt, cansock): #Function which gets the CAN message
	while 1: #infinite loop which just gets CAN messages. Put the SQL connection here.
		cf, addr = cansock.recvfrom(can_frame_size) 
		can_id, can_dlc, data = struct.unpack(can_frame_fmt, cf)
		print('Received: can_id=%x '% can_id)
		print('Received: can_dlc=%x' % can_dlc)
		print('Received: data=%s' % data)
		print('Received: can_id=%x, can_dlc=%x, data=%s' % struct.unpack(can_frame_fmt, cf)) 
	return (can_id, can_dlc, data[:can_dlc])
	
def SendCanMessage(can_frame_fmt, can_id,cansock):
	while 1:
		message = q2.get() #Gets CAN message from the queue 
		message.split(",")
		can_dlc = message[0]
		data = message[1]
		#can_dlc = len(message)/2
		#can_dlc = int(can_dlc)
		data = bytes.fromhex(data)# Think these are the send commands?
		#message = message.ljust(8, b'\x00')
		#msg1 = (str(message)).encode("utf-8")
		#print("message is")
		#print(message)
		#canmessage = struct.pack(can_frame_fmt, can_id, can_dlc, message)
		#message = b"\x00\x00"
		print(message)
		canmessage = struct.pack(can_frame_fmt, can_id, 2, data)
		cansock.send(canmessage)
		q2.task_done() #Marks the message as sent so it can move on to the next
		print("message sent")
		
db_clients_INFO = []
db_clients_IP = []
main()
