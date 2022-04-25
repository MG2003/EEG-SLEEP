import bandpower
import tkinter
from tkinter import *
from tkinter import Button, GROOVE
from threading import *


clicked = False

def click():
    global clicked
    clicked = True

def threading():
    # Call work function
    t1=Thread(target=proc)
    t1.start()
def proc():
    global clicked
    start['state'] = 'disabled'
    bandpower.run()
    
    if(clicked == False):
        
        proc()
    else:
        print('bye')
        clicked = False
        start['state'] = 'normal'
        return None
        
   
        


root = Tk()

label = Label(root, text = "EEG Sleep Diagnosis")
start = Button(root, text="START COLLECTION", command = threading, relief = GROOVE)
end = Button(root, text = "STOP COLLECTION", command = click, relief = GROOVE)
label.pack()
start.pack()
end.pack()


root.mainloop()



