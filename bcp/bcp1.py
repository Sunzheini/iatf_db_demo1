"""
IATF16949 DATABASE DEMO

31.10.2022
"""
from tkinter import *
from tkinter import colorchooser
import sqlite3


# global variables
number_of_process_steps = 1


# color picker func
def color_chooser_func():
    color = colorchooser.askcolor()     # looks like ((118, 152, 203), '#7698cb')
    root.config(background=color[1])


# create process step func
def create_process_step():
    global number_of_process_steps

    conn = sqlite3.connect("simple_iatf_manager.db")
    c = conn.cursor()

    process_step_number = Label(
        root,
        text=number_of_process_steps,
        width=3,
        height=2,
        borderwidth=2,
        relief="ridge",
    )
    process_step_number.grid(row=number_of_process_steps, column=0)

    process_name = Label(
        root,
        text="process name",
        width=12,
        height=2,
        borderwidth=2,
        relief="ridge",
    )
    process_name.grid(row=number_of_process_steps, column=1)

    process_responsible = Label(
        root,
        text="responsible..",
        width=12,
        height=2,
        borderwidth=2,
        relief="ridge",
    )
    process_responsible.grid(row=number_of_process_steps, column=2)

    process_evidences = Label(
        root,
        text="evidences..",
        width=12,
        height=2,
        borderwidth=2,
        relief="ridge",
    )
    process_evidences.grid(row=number_of_process_steps, column=3)

    c.execute("INSERT INTO iatf VALUES (:process_step_number, :process_name, :process_responsible, :process_evidences)",
              {
                  # ToDo: this was originally 'l_name': l_name.get(), because it got info from Entry with name l_name
                  'process_step_number': 1,
                  'process_name': 2,
                  'process_responsible': 3,
                  'process_evidences': 4,
              })
    conn.commit()
    conn.close()

    number_of_process_steps += 1


def display_process_steps():
    conn = sqlite3.connect("simple_iatf_manager.db")
    c = conn.cursor()
    records = c.fetchall()

    print_records = ''
    for r in records:  # records[0] is first line from database
        print_records += str(r) + '\n'
    print(print_records)
    conn.commit()
    conn.close()

# main window
# ----------------------------------------------------------------------------------------------#

root = Tk()
root.title("Simple IATF Manager")
root.eval("tk::PlaceWindow . center")
x = root.winfo_screenwidth() // 4           # 4: left edge starts from, 1/4 of screen width
y = int(root.winfo_screenheight() * 0.2)    # top edge starts from 20% of screen height
root.geometry('500x600+' + str(x) + '+' + str(y))

# window icon
icon = PhotoImage(file='staticfiles/iatf_logo.png')   # convert image
root.iconphoto(True, icon)    # change icon image

# grid on main window
titleNLabel = Label(
    root,
    width=10,
    height=2,
    text="Processes",
)
titleNLabel.grid(row=0, column=0, columnspan=2)


# buttons
# -------------------------------------------------------------------------------#

# color picker button
color_picker_button = Button(root, text='colorpicker', command=color_chooser_func)
color_picker_button.place(x=350, y=25)

# create process step button
create_process_step_button = Button(root, text='create process step', command=create_process_step)
create_process_step_button.place(x=350, y=50)

# display process steps button
display_process_steps_button = Button(root, text='display process step', command=display_process_steps)
display_process_steps_button.place(x=350, y=75)

# ToDo: delete step
# delete process step button
# delete_process_step_button = Button(root, text='create process step', command=delete_process_step)
# delete_process_step_button.place(x=350, y=100)


# database creation if it doesnt exist
# -------------------------------------------------------------------------------#
conn = sqlite3.connect("simple_iatf_manager.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS iatf(
    process_step_number integer,
    process_name text,
    process_responsible text,
    process_evidences text
    )
""")

conn.commit()
conn.close()


# -------------------------------------------------------------------------------#
# run
root.mainloop()
