"""
IATF16949 DATABASE DEMO

31.10.2022

ToDo: направих тест и грид работи във фрейм
ToDo: дали фогурите от флоучарта да са картинка наслагани (compound) в/у текста в гутийката
"""
from tkinter import *
from tkinter import colorchooser, messagebox, filedialog, ttk
import sqlite3

# ToDo class process step
# ToDo first store process steps in a dictionary then to database, so you can refer to process steps
# ToDo optimise program


# frame1.pack_propagate = False     # child widgets do not modify parent


# global variables
number_of_process_steps = 1
current_file_path = 'some file...'


def open_file_menu():
    print('openFile')


def save_file_menu():
    print('saveFile')


# new window with separate tabs
def create_window():
    new_window = Toplevel()   # new window on top of other windows, linked to a botton window
    # new_window = Tk()       # independent window
    # window.destroy()        # close the old window

    notebook = ttk.Notebook(new_window)     # manages a collection of windows and displays
    tab1 = Frame(notebook)      # new frame for tab1
    tab2 = Frame(notebook)

    notebook.add(tab1, text='tab 1')
    notebook.add(tab2, text='tab 2')
    notebook.place(x=0, y=0)

    label1 = Label(tab1, text='Hello tab1')
    label1.pack()
    label2 = Label(tab2, text='Hello tab2')
    label2.place(x=0, y=0)


# new window with flowchart on cancas
def create_flowchart_canvas():
    new_window2 = Toplevel()

    new_canvas = Canvas(new_window2, height=400, width=400)

    new_canvas.create_rectangle(10, 10, 110, 50,
                                fill='white', width=2)  # start x, y, end x, y
    new_canvas.create_line(60, 50, 60, 80,
                           width=1, fill='blue', arrow=LAST,
                           arrowshape=(5.0, 5.0, 4.0))  # start x, y, end x, y
    new_canvas.create_rectangle(10, 80, 110, 120,
                                fill='white', width=2)
    new_canvas.create_line(60, 120, 60, 150,
                           width=1, fill='blue', arrow=LAST,
                           arrowshape=(5.0, 5.0, 4.0))

    points = [60, 150, 10, 170, 60, 190, 110, 170]  # x, y, x, y, ...
    new_canvas.create_polygon(points, fill='white', outline='black', width=2)

    new_canvas.pack()


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
        bg='white',
        borderwidth=2,
        relief="ridge",
    )
    process_step_number.grid(row=number_of_process_steps, column=0)

    # depends on checkbox
    if x.get() == 1:
        special_font = 'yellow'
    else:
        special_font = 'light grey'

    # depends on textfield then on listbox
    process_name = 'blank'
    if write_text_field.get('1.0', END) != "\n":     # get the text from the textfield
        process_name = write_text_field.get('1.0', END).strip()
    else:
        if listbox.curselection()[0] == 0:
            process_name = 'terminator'
        elif listbox.curselection()[0] == 1:
            process_name = 'ordinary step'
        elif listbox.curselection()[0] == 2:
            process_name = 'decision'

    process_name = Label(
        root,
        text=process_name,
        fg='purple',
        bg=special_font,
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
        bg='white',
        borderwidth=2,
        relief="ridge",
    )
    process_responsible.grid(row=number_of_process_steps, column=2)

    # read selected file path
    global current_file_path
    evidences = current_file_path
    current_file_path = 'some file...'

    process_evidences = Label(
        root,
        text=evidences,
        width=15,
        height=2,
        bg='white',
        borderwidth=2,
        relief="ridge",
    )
    process_evidences.grid(row=number_of_process_steps, column=3)

    # ToDo: finish this - add canvas to row
    canvas = Canvas(root, height=25, width=25, bg='white')
    canvas.create_rectangle(5, 5, 20, 20, fill='white', width=2)  # start x, y, end x, y
    canvas.grid(row=number_of_process_steps, column=4)

    c.execute("INSERT INTO iatf VALUES (:process_step_number, :process_name, :process_responsible, :process_evidences)",
              {
                  # ToDo: this was originally 'l_name': l_name.get(), because it got info from Entry with name l_name
                  # get(): get string from input
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
    c.execute("SELECT *, oid FROM iatf")
    records = c.fetchall()

    print_records = ''
    for r in records:  # records[0] is first line from database
        print_records += str(r) + '\n'

    print(print_records)
    display_label = Label(root, text=print_records,
                          width=20, height=15, bg='white', borderwidth=2, relief="ridge")
    display_label.place(x=50, y=300)

    conn.commit()
    conn.close()


def delete_process_step():
    conn = sqlite3.connect("simple_iatf_manager.db")
    c = conn.cursor()
    c.execute("DELETE FROM iatf WHERE oid = " + delete_entry.get())
    conn.commit()
    conn.close()
    delete_entry.delete(0, END)   # deletes what we entered in the box


def delete_all_process_steps():

    if messagebox.askokcancel(title='delete all', message='are you sure you want to clear the database?'):   # choice
        conn = sqlite3.connect("simple_iatf_manager.db")
        c = conn.cursor()
        c.execute("DELETE FROM iatf")
        conn.commit()
        conn.close()
    else:
        return


def openfile():
    global current_file_path
    current_file_path = filedialog.askopenfilename()     # returns a string where the file is located
    print(current_file_path)
    # filepath = filedialog.asksaveasfile()     # can also save files


# main window
# ----------------------------------------------------------------------------------------------#

root = Tk()
root.title("Simple IATF Manager")

# ToDo: commented this after adding the file menu since it was not working
# root.eval("tk::PlaceWindow . center")     # option 1

# x = root.winfo_screenwidth() // 4          # 4: left edge starts from, 1/4 of screen width
# y = int(root.winfo_screenheight() * 0.2)    # top edge starts from 20% of screen height
# root.geometry('500x600+' + str(x) + '+' + str(y))

root.geometry('500x600')

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

# menu
# -------------------------------------------------------------------------------#

menubar = Menu(root)
root.config(menu=menubar)

# 'File'
fileMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='File', menu=fileMenu)       # dropdown menu

fileMenu.add_command(label='Open', command=open_file_menu)
fileMenu.add_command(label='Save', command=save_file_menu)
fileMenu.add_separator()                               # separator
#fileMenu.add_command(label='Exit', command=quit)   # 'quit' not working with pyinstaller
fileMenu.add_command(label='Exit', command=save_file_menu)

# 'Edit'
editMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Edit', menu=editMenu)

editMenu.add_command(label='New Window', command=create_window)
editMenu.add_command(label='New Flowchart', command=create_flowchart_canvas)


# frame1
# -------------------------------------------------------------------------------#

frame1 = Frame(root, bg='grey', bd=5, relief='ridge')
frame1.place(x=345, y=450)


# buttons / fields
# -------------------------------------------------------------------------------#

# color picker button
color_picker_button = Button(root, text='colorpicker', command=color_chooser_func, cursor='hand2')
color_picker_button.place(x=350, y=25)


frame_button1 = Button(frame1, text='button 1..', command=color_chooser_func)
frame_button1.pack_propagate(False)
frame_button1.pack(side='top', padx=0, pady=0)

frame_button2 = Button(frame1, text='button 2..', command=color_chooser_func)
frame_button2.pack_propagate(False)
frame_button2.pack(side='top', padx=3, pady=3, anchor='n')

# checkbutton if process is special
x = IntVar()     # datatype should reflect what is stored in the variable (BooleanVar, StringVar, etc.)
check_button = Checkbutton(
    root, text='special process', variable=x,
    onvalue=1,      # by default returns 0 or 1
    offvalue=0)     # can also have command
check_button.place(x=350, y=75)

# listbox for process step type
listbox = Listbox(root, bg='#f7ffde', selectmode=SINGLE)    # MULTIPLE: can select multiple items
listbox.place(x=350, y=100)
listbox.insert(1, 'terminator')      # items inside the listbox
listbox.insert(2, 'ordinary step')
listbox.insert(3, 'decision')
listbox.config(height=listbox.size())        # change height of listbox depending on items

# write a custom process step type
textLabel = Label(root, width=20, height=2, text="custom process step name",)
textLabel.place(x=350, y=150)
write_text_field = Text(root, height=3, width=6)
write_text_field.place(x=350, y=175)

# create process step button
create_process_step_button = Button(root, text='create process step',
                                    activebackground='grey',
                                    command=create_process_step)
create_process_step_button.place(x=350, y=200)

# display process steps button
display_process_steps_button = Button(root, text='display process step', command=display_process_steps)
display_process_steps_button.place(x=350, y=250)

# delete process step button
delete_entry = Entry(root, width=20)
delete_entry.place(x=350, y=300)
delete_process_step_button = Button(root, text='delete process step', command=delete_process_step)
delete_process_step_button.place(x=350, y=325)

# delete all process steps button
delete_all_process_steps_button = Button(root, text='delete all processes', command=delete_all_process_steps)
delete_all_process_steps_button.place(x=350, y=350)

# open file path
open_file_button = Button(root, text='open file', command=openfile)
open_file_button.place(x=350, y=400)


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
