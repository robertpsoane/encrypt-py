from programfiles.encrypt import RSAEncryptor as RSA
from programfiles.buttons import *
import tkinter as tk

## Initiating Encryptor
rsa = RSA()

##### Creating GUI
gui = tk.Tk()
gui.title('Password Manager')
gui.configure(background='MOCCASIN')

## Creating Buttons
new_record_button = tk.Button(gui, text='New File', command=newFile)
load_record_button = tk.Button(gui, text='Load File', command=loadFile)
add_record_button = tk.Button(gui, text='Add Record', command=addRecord)
remove_record_button = tk.Button(gui, text='Remove Record', command=removeRecord)
help_button = tk.Button(gui, text='Help', command=helpButton)

buttons = [new_record_button,
    load_record_button,
    add_record_button, 
    remove_record_button,
    help_button
    ]

for button in buttons:
    button.pack()

tk.mainloop()