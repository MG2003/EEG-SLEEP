import bandpower as bandpower
import tkinter
from tkinter import *
from tkinter import Button, GROOVE
from threading import *
import time

starttime = time.time()


clicked = False

def click():
    global clicked
    clicked = True
def get_timestamp():
    return str(round(time.time()-starttime, 2))
def threading():
    # Call work function
    information.insert("end", get_timestamp() + ": Starting Data Collection\n")
    t1=Thread(target=proc)
    t1.start()
def proc():
    global clicked
    start['state'] = 'disabled'
    info = bandpower.run()     
    information.insert("end", get_timestamp() + ": Data Received\n")
    information.insert("end", "Alpha band power: " + str(round(info["alpha"],2))+ "\n")
    information.insert("end", "Theta band power: " + str(round(info["theta"],2))+"\n")
    information.insert("end", "Alpha/Theta Ratio: " + str(round(info["alpha"]/info["theta"], 2)) + "\n")
    information.see("end")
    if(clicked == False):    
        proc()
    else:
        print('bye')
        clicked = False
        start['state'] = 'normal'
        return None
        
   
        
fontfamily = {
    "main": 8,
    "title": 17

}

root = Tk()
root.geometry("350x350") 
label = Label(root, text = "EEG Sleep Diagnosis", font = ("Arial", fontfamily["title"]))
instructions = Label(root, text="Insert bluetooth dongle into computer, \nmake sure EEG is on, and press start collection")
information = Text(root, borderwidth= 2, relief = GROOVE, width = 40, height = 10)
start = Button(root, text="START COLLECTION", command = threading, relief = GROOVE, width = 17, height = 3, font = ("Arial", fontfamily["main"]))
end = Button(root, text = "STOP COLLECTION", command = click, relief = GROOVE, width = 17, height = 3, font = ("Arial", fontfamily["main"]))
label.pack(padx = 10, pady = 10)
instructions.pack()
information.pack(pady = 5)
start.pack(padx = 30, side = LEFT)
end.pack(padx = 30, side = RIGHT)



root.mainloop()



