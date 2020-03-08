from tkinter import *

var = IntVar()
master = Tk()
var.set(1)

entry_text = StringVar()
entry_text.set("###")

def quit_loop():
    print ("Selection:",var.get())
    global selection
    selection = var.get()

    if selection == 2:
        selection = entry_text.get()

    master.quit()

# Add columnspan to these widgets
Label(master, text = "Select OCR language").grid(row=0, sticky=W, columnspan=3)
Radiobutton(master, text = "default", variable=var, value = 1).grid(row=1, sticky=W, columnspan=3)

# Order these widgets in their appropriate columns
Radiobutton(master, variable=var, value = 2).grid(row=2, sticky=W, column=0)
Label(master, text="Enter value:").grid(row=2, sticky=W, column=1)
Entry(master, textvariable=entry_text).grid(row=2, sticky=W, column=2)

# Example of what happens without columnspan
Button(master, text = "OK", command=quit_loop).grid(row=3, sticky=W)

master.mainloop()

print (selection)  