from programfiles.encrypt import RSAEncryptor as RSA
from programfiles.buttons import ButtonFunctions
import tkinter as tk

## Initiating Main Classes
rsa = RSA()
BF = ButtonFunctions(rsa)

##### Important Variables
screen_width = 640
screen_height = 420
screen_size = screen_width, screen_height
background_colour = 'MOCCASIN'

##### Creating GUI
main_gui = tk.Tk()
main_gui.title('Password Manager')
main_gui.configure(background=background_colour)

##### Setting Up Frames
## Main Frame
main_frame = tk.Frame(
    main_gui, 
    height = screen_height, 
    width=screen_width,
    background=background_colour).grid(row=0, column = 0)

## Top Frame (Frame containing buttons and password tables)
top_frame = tk.Frame(
    main_frame,
    height = (3/4) * screen_height,
    width = screen_width,
    background=background_colour
    )

## Bottom Frame (Frame containing path and key)
bottom_frame = tk.Frame(
    main_frame,
    height = (1/4) * screen_height,
    width = screen_width,
    background=background_colour
    )

## Buttom Frame
button_frame = tk.Frame(
    top_frame,
    height=(3/4) * screen_height,
    width=(1/5)*screen_width,
    background=background_colour
    )

## Password Table Frame
table_frame = tk.Frame(
    top_frame,
    height = (3/4) * screen_width,
    width = (4/5) * screen_width,
    background=background_colour
    )

## Keys Frame
keys_frame = tk.Frame(
    bottom_frame,
    height = (1/4) * screen_height,
    width = screen_width,
    background=background_colour,
    )

## Packing frames
top_frame.pack_propagate(0) 
top_frame.grid(row=0, column=0)

bottom_frame.pack_propagate(0) 
bottom_frame.grid(row=1, column=0)

button_frame.pack_propagate(0) 
button_frame.grid(row=0, column=0)

table_frame.pack_propagate(0) 
table_frame.grid(row=0, column=1)

keys_frame.pack_propagate(0) 
keys_frame.grid(row=0, column=0)

##### Setting Up Buttons
## Creating Buttons
new_record_button = tk.Button(
    button_frame,
    text='New File',
    command=BF.newFile,
    width = 15
    )

load_record_button = tk.Button(
    button_frame,
    text='Load File',
    command=BF.loadFile,
    width = 15
    )

add_record_button = tk.Button(
    button_frame,
    text='Add Record',
    command=BF.addRecord,
    width = 15
    )

remove_record_button = tk.Button(
    button_frame,
    text='Remove Record',
    command=BF.removeRecord,
    width = 15
    )

change_record_button = tk.Button(
    button_frame,
    text='Change Record',
    command=BF.changeRecord,
    width = 15
    )

help_button = tk.Button(
    button_frame,
    text='Help',
    command=BF.helpButton,
    width = 15
    )

## Packing Buttons
buttons = [new_record_button,
    load_record_button,
    add_record_button, 
    remove_record_button,
    change_record_button,
    help_button
    ]

for k in range(len(buttons)):
    buttons[k].grid(row=k, column=0, pady = screen_height/50)



tk.mainloop()