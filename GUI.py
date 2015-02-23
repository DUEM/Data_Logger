from tkinter import *    
import socket, sys, threading
from queue import Queue
import numpy as np
import pylab
import matplotlib.pyplot as plot
from matplotlib.pylab import subplots,close
from matplotlib import cm
import time,sys,os
from datetime import datetime

# allows communication between threads
q = Queue()	 # talk to communication thread
q.join()
q2 = Queue()    # talk to live plot battery thread
q2.join()
q3 = Queue()    # talk to saving csv battery thread
q3.join()
q4 = Queue()    # talk to live plot speed thread
q4.join()
q5 = Queue()    # talk to  saving csv speed thread
q5.join()
q6 = Queue()    # talk to  live plot temperature thread
q6.join()
q7 = Queue()    # talk to  saving csv temperature thread
q7.join()
q8 = Queue()    # monitor can messages
q8.join()

###################### Sending/Recieving data bit ###########################
def comunication(host = "10.245.124.17",port = 51432):
        ## CLIENT
        
        # host = input()
        # port = input() ?
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # can be inside of a while loop
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # ^ reconnects using same ip ^
        while 1:
        	t = True
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
                		t = False
                		msg2 = ""
                	if t == True:
            			try:
                			msg1 = sock.recv(2048)
                			if len(msg1):
                        			msg2 = msg1.decode("utf-8")
                        			print(msg2)
                        	#OutShell.insert(END,msg2+'\n')
                        	#OutShell.see(END)
                        	
            			except:
                			print("Failed to recieve the message")
                			t = False
                	if t == True:
                		if "_COM_LIVE_PLOT_BAT_" in msg2:
                            		q2.put(msg2)
                        	elif  "_COM_SAVE_BAT_" in msg2:
                                	q3.put(msg2)
                        	elif "_COM_LIVE_PLOT_SPEED_" in msg2:
                                	q4.put(msg2)
                        	elif "_COM_SAVE_SPEED_" in msg2:
                                	q5.put(msg2)
                        	elif "_COM_LIVE_PLOT_TEMP_" in msg2:
                                	q6.put(msg2)
                        	elif "_COM_SAVE_TEMP_" in msg2:
                                	q7.put(msg2)
                        	elif "_MONITOR_CAN_BUS_" in msg2:
                                	q8.put(msg2)
                        	else:
                                	OutShell.insert(END,'\n'+'>'*80+'\n'+msg2+'\n'+'<'*80+'\n\n')
                                	OutShell.see(END)
        	sock.close()

comm = threading.Thread(target = comunication) #seperate thread for the communicating with the server
comm.daemon = True
comm.start()
############################################################################

################################ Can Monitor ###############################
def can_monitor(Qout):
        message = Qout.get() # get command to send forr more data
        print(message)
        Qout.task_done()
        stop_message = "_STOP_"
        prevDat = "a"
        while True:
                
                data = Qout.get()
                if data == stop_message:
                        print("CLOSE")
                        break
                data = data.replace(message,"")
                if data != prevDat:
                        OutShell.insert(END,data+' \n')
                        OutShell.see(END)
                        prevDat = data
                Qout.task_done()
                q.put(message)
################################# Live Plot #################################
def bat_plot(Qout):
        message = Qout.get() # get command to send forr more data
        Qout.task_done()
        variable = Qout.get() # get variable name for filenames
        Qout.task_done()
        #plot.ion()
        pylab.ion()
        #fig = plot.figure()
        fig = pylab.figure()
        fig.show()
        stop_message = "_STOP_"
        while True:
                data = Qout.get()
                if data == stop_message:
                        # save figure then close
                        Time = datetime.utcnow().strftime("%d-%m-%Y")
                        filename = "SavedPlots/"+variable+" - " + Time + ".png"
                        fig.savefig(filename)
                        OutShell.insert(END,'Data saved to file: ' + filename +'\n')
                        OutShell.see(END)
                        close(fig)
                        break
                data = data.replace(message,"")
                try:
                        x = time.clock()
                        y = float(data)
                        #time.sleep(0.5)
                        pylab.scatter(x,y)
                        pylab.draw()
                        #time.sleep(0.5)
                except:
                        break
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
                data = data.replace(message,"")
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
        Inmessage = CanInput.get()
        #if inpType == 0:
        #        message = int(Inmessage, 16)
        #else:
                #message = int(Inmessage,16)
        message = Inmessage
        OutShell.insert(END,'Sending Can Message: '+str(message)+'\n') 
        OutShell.see(END)
        message = "_SEND_CAN_MESSAGE_" + str(message) #add pefix so sever knows what sort of data it is
        q.put(message)
        
        return 1

def send_command(): # funcion that sends commands
        message = LoggerInput.get()
        OutShell.insert(END,'Sending Server Command: '+message+'\n') 
        OutShell.see(END)
        message = "COM" + message
        q.put(message)
        return 1

def SendCommands(command, but1, but2): # funcion that sends commands
        message = command
        OutShell.insert(END,'Sending Server Command: '+message+'\n') 
        OutShell.see(END)
        q.put(message)
        toggle(but1)
        toggle(but2)
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
        qout.put(variable) 
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
        OutShell.insert(END,'Saving' + variable + 'data to file: '+filename+'\n') 
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

def CanMonitor(variable, command, qout, enab_but, disab_but):
         # clears the que before it is used
        while qout.empty() == False:            
                qout.get()
                qout.task_done()
        #start thread
        MON = threading.Thread(target = lambda: can_monitor(qout))
        MON.daemon = True
        MON.start()

        message = command
        qout.put(message)
        # request data from server
        q.put(message)

        # toggle buttons
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

        #Live Plot Speed
        but7=Button(Inputs, text='Live Plot Speed',  width=30, state='normal')  
        but7.grid(row=4,column=0)
        #Stop Live Plot Speed
        but8=Button(Inputs, text='Stop Live Plot Speed',  width=30, state='disabled')  
        but8.grid(row=4,column=1)

        but7.config( command= lambda: LivePlot("Speed","_COM_LIVE_PLOT_SPEED_",q4,but7,but8))
        but8.config( command= lambda: SendStopMessage(q4,but7,but8))

        #Save Speed Data To CSV
        but9=Button(Inputs, text='Save Speed Data To CSV',  width=30, state='normal')  
        but9.grid(row=5,column=0)
        #Stop Saving Speed Data To CSV
        but10=Button(Inputs, text='Stop Saving Speed Data To CSV',  width=30, state='disabled')  
        but10.grid(row=5,column=1)

        but9.config( command= lambda: SaveDataCSV('Speed', "_COM_SAVE_SPEED_", q5, but9, but10))
        but10.config( command= lambda: SendStopMessage(q5, but9, but10))        

        #Monitor All CAN Activity
        but11=Button(Inputs, text='Monitor All CAN Activity',  width=30, state='normal')  
        but11.grid(row=6,column=0)
        #Stop Monitoring All CAN Activity
        but12=Button(Inputs, text='Stop Monitoring All CAN Activity',  width=30, state='disabled')  
        but12.grid(row=6,column=1)
        
        but11.config( command= lambda: CanMonitor('Can Message', "_MONITOR_CAN_BUS_",q8, but11, but12))
        but12.config( command= lambda: SendStopMessage(q8, but11, but12))

        #Live Plot Temperature
        but13=Button(Inputs, text='Live Plot Temperature',  width=30, state='normal')  
        but13.grid(row=7,column=0)
        #Stop Live Plot Temperature
        but14=Button(Inputs, text='Stop Live Plot Temperature',  width=30, state='disabled')  
        but14.grid(row=7,column=1)

        but13.config( command= lambda: LivePlot("Temperature","_COM_LIVE_PLOT_TEMP_",q6,but13,but14))
        but14.config( command= lambda: SendStopMessage(q6,but13,but14))

        #Save Temperature Data To CSV
        but15=Button(Inputs, text='Save Temperature Data To CSV',  width=30, state='normal')  
        but15.grid(row=8,column=0)
        #Stop Saving Temperature Data To CSV
        but16=Button(Inputs, text='Stop Saving Temperature Data To CSV',  width=30, state='disabled')  
        but16.grid(row=8,column=1)

        but15.config( command= lambda: SaveDataCSV('Temperature', "_COM_SAVE_TEMP_", q7, but15, but16))
        but16.config( command= lambda: SendStopMessage(q7, but15, but16))
        
        return 1


root=Tk()            #creates window
root.title('USM system (Ultimate Solar-car Management system)') #adds title to window

Inputs=LabelFrame(root,text='Command Area',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Inputs.grid(row=0)

inpType = 0

################ TEXT FIELDS ###################	
#HAVE TO BE GLOBAL :(
CanInput = Entry(Inputs, width=30)
CanInput.grid(row = 0, column = 0)
CanInput.focus_set()

LoggerInput = Entry(Inputs, width=30)
LoggerInput.grid(row = 1, column = 0)

#Radio Button
hexSelect = Radiobutton(Inputs, text="Hex", variable=inpType, value=0)
hexSelect.grid(row = 0, column = 3)
#Radio Button
AsciiSelect = Radiobutton(Inputs, text="Ascii", variable=inpType, value=1)
AsciiSelect.grid(row = 1, column = 3)

##################################################
Buttons()

Outputs=LabelFrame(root,text='Output Terminal',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Outputs.grid(row=0, column=1)

OutShell = Text(Outputs)
OutShell.grid(row=0,column=0)

root.mainloop()
