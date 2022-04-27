from turtle import bgcolor
import bandpower as bandpower
import tkinter
from tkinter import *
from tkinter import Button, GROOVE
from threading import *
import time
import simpleaudio as sa
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
    if(info["alpha"]/info["theta"] < 0.9):
      information.insert("end", "SLEEP DETECTED, ISSUING ALERT\n")  
      status['bg'] = '#c93a44'
      wave_obj = sa.WaveObject.from_wave_file("ding.wav")
      play_obj = wave_obj.play()
      play_obj.wait_done()
    else:
        status['bg'] = '#57ab6d'
    information.see("end")
    if(clicked == False):    
        proc()
    else:
        information.instert("end", get_timestamp()+ ": Exiting session\n")
        information.see("end")
        print('bye')
        clicked = False
        start['state'] = 'normal'
        return None
        
   
        
theme = {
    "main": 8,
    "title": 17,
    "labelcol": '#ffe8f0'

}

root = Tk()
root.configure(background='pink')
root.geometry("350x375") 
label = Label(root, text = "EEG Sleep Diagnosis", font = ("Arial", theme["title"]), bg = theme["labelcol"])
instructions = Label(root, text="Insert bluetooth dongle into computer, \nmake sure EEG is on, and press start collection", bg = theme["labelcol"])
status = Frame(root, bg = "#57ab6d", height = 30, width = 200)
information = Text(root, borderwidth= 2, relief = GROOVE, width = 40, height = 7, bg = theme["labelcol"])
start = Button(root, text="START COLLECTION", command = threading, relief = GROOVE, width = 17, height = 3, font = ("Arial", theme["main"]), bg = theme["labelcol"])
end = Button(root, text = "STOP COLLECTION", command = click, relief = GROOVE, width = 17, height = 3, font = ("Arial", theme["main"]), bg = theme["labelcol"])
label.pack(padx = 15, pady = 10)

instructions.pack(pady = 5)
status.pack(pady = 10)
information.pack(pady = 5)
start.pack(padx = 30, side = LEFT)
end.pack(padx = 30, side = RIGHT)



root.mainloop()



