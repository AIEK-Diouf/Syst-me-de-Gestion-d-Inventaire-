'''
Created on MARCH 11, 2026
@author: AIEK-DIOUF

'''

from tkinter import *

root = Tk()


# creating a label widget
myLabel1 = Label(root, text="Hello world!").grid(row=0, column=0)
myLabel2 = Label(root, text="Systeme-de-Gestion-d-Inventaire")

'''
# make it into the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=1)
'''
myButton = Button(root, text="Click me!", padx=10, pady=10 )







root.mainloop()