from tkinter import *    
import socket, sys, threading
from queue import Queue
import numpy as np
import matplotlib.pyplot as plot
import time,sys,os
from datetime import datetime

# allows communication between threads
q = Queue()	 # talk to communication thread
q.join()
q2 = Queue() # talk to live plot battery thread
q2.join()
q3 = Queue() # talk to saving csv battery thread
q3.join()
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
                        #OutShell.insert(END,msg2+'\n')
                        #OutShell.see(END)
                        if "_PLOT_BAT_" in msg2:
                            q2.put(msg2)
                        elif  "_SAVE_BAT_" in msg2:
                                q3.put(msg2)
                        else:
                                OutShell.insert(END,msg2+'\n')
                                OutShell.see(END)
            except:
                print("Failed to recieve the message")
        sock.close()

comm = threading.Thread(target = comunication) #seperate thread for the communicating with the server
comm.daemon = True
comm.start()
############################################################################

################################# Live Plot #################################
def bat_plot(Qout):
        message = Qout.get() # get command to send forr more data
        print(message)
        Qout.task_done()
        print(message)
        plot.ion()
        fig = plot.figure()
        fig.show()
        stop_message = "_STOP_"
        while True:
                data = Qout.get()
                if data == stop_message:
                        # save figure then close
                        Time = datetime.utcnow().strftime("%d-%m-%Y")
                        filename = "SavedPlots/bat - " + Time + ".png"
                        fig.savefig(filename)
                        OutShell.insert(END,'Data saved to file: ' + filename +'\n')
                        OutShell.see(END)
                        break
                data = data.replace("_PLOT_BAT_","")
                try:
                        plot.scatter(time.clock(),float(data))
                        plot.draw()
                except:
                        a = 1
                Qout.task_done()
                q.put(message)
				

#########################################################################################################################
################################ CSV STUFF ###############################
def CSVsave(qout):
        file = qout.get() #get file name
        qout.task_done()
        message = qout.get() # get command to send for more data
        qout.task_done()
        stop_message = "_STOP_"
        print(file)
        print(message)
        while True:
                data = qout.get()
                if data == stop_message:
                        break
                data = data.replace("_SAVE_BAT_","")
                try:
                        f=open(file,'a')
                        f.write(str(time.clock())+','+str(data)+'\n')
                        f.close()
                except:
                        a=1
                qout.task_done()
                q.put(message)
        return 1

##########################################################################
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
################################################################

# general structure for LivePlot and SaveDataCSV
# variable = what file will be called (CSV ONLY)
# command = what message it sends to server
# qout = which que will be used to talk to thread
# enab_but = the button to un-grey
# disab_but = button to be greyed out

# buttons can go in any way round the state is toggled

################################################################

def LivePlot(variable, command, qout, enab_but, disab_but): 
        # clears the que before it is used
        while qout.empty() == False:            
                qout.get()
                qout.task_done()
        #placing command into empty que so it is the first message to be read by the thread
        message = command
        qout.put(message)
        # start thread
        BatPlot = threading.Thread(target = lambda: bat_plot(qout))
        BatPlot.daemon = True
        BatPlot.start()
        # printing to output terminal
        OutShell.insert(END,'Plotting: '+variable+'\n') 
        OutShell.see(END)
        # send first request to server
        q.put(message)
        # toggle buttons
        toggle(enab_but)
        toggle(disab_but)
        return 1

def SaveDataCSV(variable, command, qout, enab_but, disab_but): 
        # clears the que before it is used
        while qout.empty() == False:            
                qout.get()
                qout.task_done()
        # getting the date and creating the file
        Time = str(time.ctime())
        Time = datetime.utcnow().strftime("%d-%m-%Y")
        filename = 'data/'+variable+'-'+Time+'.csv'
        f = open(filename,'a')
        f.close()
        #printing to output terminal
        OutShell.insert(END,'Saving data to file: '+filename+'\n') 
        OutShell.see(END)
        #start thread
        CSV = threading.Thread(target = lambda: CSVsave(qout))
        CSV.daemon = True
        CSV.start()
        # putting filename and command into the queue 
        qout.put(filename)
        message = command
        qout.put(message)
        # request data from server
        q.put(message)
        #toggle buttons
        toggle(enab_but)
        toggle(disab_but)
        return 1

def SendStopMessage(qout, enab_but, disab_but):
        #send stop message
        message = "_STOP_"
        qout.put(message)
        #toggle buttons
        toggle(enab_but)
        toggle(disab_but)
        return 1

def toggle(but): # toggles buttons states
        # checks if disabled
        if but.config('state')[-1] == 'disabled':
                but.config(state='normal')
        else:
                but.config(state='disabled')

def Buttons(): # creates buttons

        #Send CAN Message
        but1=Button(Inputs, text='Send Can Message', command=send_can, width=30)                          
        but1.grid(row=0,column=1)

        #Send Command to Datalogger
        but2=Button(Inputs, text='Send Command to Datalogger', command=send_command, width=30)                            
        but2.grid(row=1,column=1)

        #Live Plot Battery Data
        but3=Button(Inputs, text='Live Plot Battery Data', width=30, state='normal')                            
        but3.grid(row=2,column=0)

        #Stop Live Plot Battery Data
        but4=Button(Inputs, text='Stop Live Plot Battery Data',  width=30, state='disabled') 
        but4.grid(row=2,column=1)
        # commands seperated from rest of button definition so both buttons have been declared before use
        but3.config( command= lambda: LivePlot("Battery","_COM_LIVE_PLOT_BAT_",q2,but4,but3))
        but4.config( command= lambda: SendStopMessage(q2,but3,but4))

        #Save Battery Data To CSV
        but5=Button(Inputs, text='Save Battery Data To CSV',  width=30, state='normal')  
        but5.grid(row=3,column=0)

        #Stop Saving Battery Data To CSV
        but6=Button(Inputs, text='Stop Saving Battery Data To CSV',  width=30, state='disabled')  
        but6.grid(row=3,column=1)

        but5.config( command= lambda: SaveDataCSV('Battery', "_COM_SAVE_BAT_", q3, but6, but5))
        but6.config( command= lambda: SendStopMessage(q3, but5, but6))
        
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

Outputs=LabelFrame(root,text='Output Terminal',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Outputs.grid(row=0, column=1)

OutShell = Text(Outputs)
OutShell.grid(row=0,column=0)



root.mainloop()


