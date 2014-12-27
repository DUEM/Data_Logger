import tkinter as tk       

def send_can(): # function that sends can message
    return 1

def send_command(): # funcion that sends commands
    return 1

def execute():
    return 1

root=tk.Tk()            #creates window
root.title('USM system (Ultimate Solar-car Management system)') #adds title to window

Inputs=tk.LabelFrame(root,text='Command Area',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Inputs.grid(row=0)

but1=tk.Button(Inputs, text='Send Custom Can Message', command=send_can, width=30)                          #button to load seq1 calls function o() 
but1.grid(row=0,column=0)

but2=tk.Button(Inputs, text='Send Commands to Datalogger', command=send_command, width=30)                            #loads seq2 calls function p() 
but2.grid(row=1,column=0)

run=tk.Button(Inputs, text='Please Click Here to Send', command=execute, width=30)          # run button calls function execute() 
run.grid(row=2,column=0)

but3=tk.Button(Inputs, text='Need More Buttons Because thier Cool', width=30)                            #loads seq2 calls function p() 
but3.grid(row=3,column=0)

filler = tk.Canvas(Inputs,height=170,width=170)
filler.grid(column=1)

Outputs=tk.LabelFrame(root,text='Output Terminal',height=200,width=200, padx=5, pady=5)      #creates a frame where the input widgets will go
Outputs.grid(row=0, column=1)


root.mainloop()
