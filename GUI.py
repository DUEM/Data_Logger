from tkinter import *    
import socket, sys, threading
from queue import Queue
import numpy as np
import matplotlib.pyplot as plot
import time

# allows communication between threads
q = Queue()	 # talk to communication thread
q.join()
q2 = Queue() # talk to live plot battery thread
q2.join()

###################### Sending/Recieving data bit ###########################
def comunication():
        ## CLIENT
        t = True
        host = "localhost"
        port = 51423
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host,port)) # sock.connec_ex((host,port)) !!!
        except:
            print("Something is wrong with connecting to the server at %d." % (port))
            sock.close()
            t = False

        while t:
            try:
                message1 = q.get()#str(input("Input: "))
                if message1.lower() == "_exit_":
                        t = False
                sock.sendall(message1.encode("utf-8"))
                q.task_done()
            except:
                print("Failed to send the message")

            try:
                msg1 = sock.recv(2048)
                if len(msg1):
                    msg2 = msg1.decode("utf-8")
                    print(msg2)
                    if "_BAT_" in msg2:
                            q2.put(msg2)
            except:
                print("Failed to recieve the message")
        sock.close()

comm = threading.Thread(target = comunication) #seperate thread for the communicating with the server
comm.daemon = True
comm.start()
############################################################################

################################# Live Plot #################################
def bat_plot():
        plot.ion()
        fig = plot.figure()
        fig.show()
        stop_message = "_STOP_"
        while True:
                data = q2.get()
                if data == stop_message:
                        # save figure then close
                        # saving bit doesnt work
                        filename = "bat - " + time.ctime() + ".png"
                        fig.savefig(filename)
                        break
                data = data.replace("_BAT_","")
                try:
                        plot.scatter(time.clock(),float(data))
                        plot.draw()
                except:
                        a = 1
                q2.task_done()
                # requests more data to plot
				message = "_COM_LIVE_PLOT_BAT_"
                q.put(message)
				

#########################################################################################################################
################################ GUI STUFF THINGS ABOUT TO GET CRAY #########################################

def send_can(): # function that sends can message
        message = CanInput.get()
        message = "_SEND_CAN_MESSAGE_" + message #add pefix so sever knows what sort of data it is
        q.put(message)
        return 1

def send_command(): # funcion that sends commands
	message = LoggerInput.get()
	message = "COM" + message
	q.put(message)
	return 1
def LivePlotBat():
        BatPlot = threading.Thread(target = bat_plot)
        BatPlot.daemon = True
        BatPlot.start()
        message = "_COM_LIVE_PLOT_BAT_"
        q.put(message)
        return 1

def StopLivePlotBat():
        message = "_STOP_"
        q2.put(message)
        return 1

def Buttons(): # creates buttons

        #Send CAN Message
        but1=Button(Inputs, text='Send Can Message', command=send_can, width=30)                          #button to load seq1 calls function o()
        but1.grid(row=0,column=1)

        #Send Command to Datalogger
        but2=Button(Inputs, text='Send Command to Datalogger', command=send_command, width=30)                            #loads seq2 calls function p() 
        but2.grid(row=1,column=1)

        #Live Plot Battery Data
        but3=Button(Inputs, text='Live Plot Battery Data', command=LivePlotBat, width=30)                            #loads seq2 calls function p() 
        but3.grid(row=2,column=0)

        #Stop Live Plot Battery Data
        but3=Button(Inputs, text='Stop Live Plot Battery Data', command=StopLivePlotBat, width=30)                            #loads seq2 calls function p() 
        but3.grid(row=2,column=1)
        return 1


root=Tk()            #creates window
root.title('USM system (Ultimate Solar-car Management system)') #adds title to window

Inputs=LabelFrame(root,text='Command Area',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Inputs.grid(row=0)

################ TEXT FIELDS ###################	
#HAVE TO BE GLOBAL :(
CanInput = Entry(Inputs, width=30)
CanInput.grid(row = 0, column = 0)
CanInput.focus_set()

LoggerInput = Entry(Inputs, width=30)
LoggerInput.grid(row = 1, column = 0)
##################################################
Buttons()
filler = Canvas(Inputs,height=170,width=170)
filler.grid(column=1)

Outputs=LabelFrame(root,text='Output Terminal',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Outputs.grid(row=0, column=1)

root.mainloop()


