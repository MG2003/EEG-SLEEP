import bandpower as bandpower
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

    if(bandpower.run()==0):
        print('success')

    else:
        print('fail')
        

    if(clicked == False):    
        proc()
    else:
        print('bye')
        clicked = False
        start['state'] = 'normal'
        return None
        
   
        


root = Tk()
root.geometry("400x400") 
label = Label(root, text = "EEG Sleep Diagnosis", font = ("Arial", 17))
start = Button(root, text="START COLLECTION", command = threading, relief = GROOVE, width = 17, height = 3)
end = Button(root, text = "STOP COLLECTION", command = click, relief = GROOVE, width = 17, height = 3)
label.pack(padx = 10, pady = 10)
start.pack(padx = 30, pady = 10, side = tkinter.LEFT)
end.pack(padx = 30, pady = 10, side = tkinter.LEFT)


root.mainloop()



