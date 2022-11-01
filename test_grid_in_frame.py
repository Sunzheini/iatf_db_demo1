"""
IATF16949 DATABASE DEMO

31.10.2022
"""
from tkinter import *
from tkinter import colorchooser, messagebox, filedialog, ttk
import sqlite3

root = Tk()
root.title("Simple IATF Manager")
root.geometry('500x600')

# frame1
frame1 = Frame(root, bg='light grey', bd=5, relief='ridge')
frame1.place(x=5, y=5, width=300, height=300)

# grid
titleNLabel = Label(
    frame1,
    width=10,
    height=2,
    text="Processes",
)
titleNLabel.grid(row=0, column=0)

process_step_number = Label(
    frame1,
    text="rrrr",
    width=5,
    height=2,
    bg='white',
    borderwidth=2,
    relief="ridge",
)
process_step_number.grid(sticky="E", row=1, column=0)

process_rrr = Label(
    frame1,
    text="rrrrrrrff",
    width=5,
    height=2,
    bg='white',
    borderwidth=2,
    relief="ridge",
)
process_rrr.grid(sticky="W", row=2, column=0)

root.mainloop()
