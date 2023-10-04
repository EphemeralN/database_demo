from logging import root
from tkinter import ttk
import sqlite3
from window import Window
from mainwindow import MainAppWindow
from tkinter import *
import os.path, time

root = Tk()

root.title('China Auto CAAS Functional Safety DataBase')
# root.iconbitmap('D:\Henglong.ico')
#root.geometry('600*400')
width = 600
height = 400
g_screenwidth = root.winfo_screenwidth()
g_screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (g_screenwidth-width)/2, (g_screenheight-height)/2)
root.geometry(alignstr)

root.minsize(width, height)

# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(fill="both",expand="yes",pady=5,anchor = "w", side = "top")

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
style = ttk.Style()
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack(fill="both",expand="yes",padx = 5 ,pady=5,anchor = "n", side = "top")
# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Project", "Safety Goal ID", "Safety Goal")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Project", anchor=W, width=150)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Project", text="Project", anchor=W)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

# Add Record Entry Boxes
data_frame = LabelFrame(root, text="")
data_frame.pack(fill="x", expand="yes", padx=20, pady = 5,anchor = 's')
fn_label = Label(data_frame, text="New Project Name")
fn_label.pack(padx=10, pady=5,anchor='w')
fn_entry = Entry(data_frame)
fn_entry.pack(fill="x", expand="yes", padx=10, pady=3)


def query_database_and_show():
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('tree_crm.db')

    # Create a cursor instance
    c = conn.cursor()

    # Fetch all tables
#     sql_query = """SELECT name FROM sqlite_master  
# WHERE type='table';"""

    # Fetch unique project names
    sql_query = """SELECT DISTINCT ProjectName FROM Projects;
"""

    c.execute(sql_query)
    records = c.fetchall()

    # Add our data to the screen
    global count
    count = 0

    # for record in records:
    #	print(record)

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[0]),
                        tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[0]),
                        tags=('oddrow',))
        # increment counter
        count += 1 

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

query_database_and_show()

def open_window():
    # Grab the record number
    selected = my_tree.focus()

    # TODO: change the tb_name to project_name
    # tb_name1 = my_tree.item(selected)['values']
    # print(tb_name1)
    project_name = my_tree.item(selected)['values'][0]
    # print(tb_name2)

    # window = MainAppWindow(root, tb_name2)
    window = MainAppWindow(project_name)


# Update record
def create_table():
    # Fetch the project name from the entry
    project_name = fn_entry.get()
    subproject_table_name = project_name.replace(" ", "") + "_Table"  # Transforming "My Project" to "MyProject_Table"

    # Connect to the database
    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    # Insert the new project into the Projects table
    c.execute("INSERT INTO Projects (ProjectName, SubProjectTableName) VALUES (?, ?)", (project_name, subproject_table_name))

    # Commit changes
    conn.commit()
    conn.close()

    # Clear entry boxes
    fn_entry.delete(0, END)

    # Refresh the treeview
    query_database_and_show()


# def delete_table():
#     # Get the selected project name
#     selected = my_tree.focus()
#     project_name = my_tree.item(selected)['values'][0]

#     # Connect to the database
#     conn = sqlite3.connect('tree_crm.db')
#     c = conn.cursor()

#     # Delete the selected project from the Projects table
#     c.execute("DELETE FROM Projects WHERE ProjectName=?", (project_name,))

#     # Commit changes
#     conn.commit()
#     conn.close()

#     # Refresh the treeview
#     query_database_and_show()

def delete_table():
    selected = my_tree.focus()
    tb_name = my_tree.item(selected)['values'][0]

    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    try:
        print("Attempting to delete:", tb_name)  # Debugging

        # Fetch all the SubProjectTableNames associated with the selected ProjectName
        c.execute("SELECT SubProjectTableName FROM Projects WHERE ProjectName=?", (tb_name,))
        subprojects = c.fetchall()
        print(f"tb_name: {tb_name}")
        print("Subprojects:", subprojects)  # Debugging

        # Delete each sub-table
        for subproject in subprojects:
            subproject_table_name = subproject[0]
            c.execute("DROP TABLE {}".format(subproject_table_name))
            print(f"Deleted subproject table: {subproject_table_name}")  # Debugging

        # Remove the records from the Projects table
        c.execute("DELETE FROM Projects WHERE ProjectName=?", (tb_name,))
        print(f"Deleted project: {tb_name}")  # Debugging

        conn.commit()
        query_database_and_show()

    except sqlite3.Error as e:
        # Show error message
        tk.messagebox.showerror("Error", f"Failed to delete {tb_name} and its associated subprojects. Error: {e}")
        print(f"Failed to delete {tb_name} and its associated subprojects. Error: {e}")
    finally:
        conn.close()




# Add Buttons
button_frame = LabelFrame(root, text="Commands")
# button_frame.place(x = 5, rely = 0.85) 
button_frame.pack(fill="x", expand="yes", padx=20,anchor = "s", side = "bottom")

button_open = Button(button_frame,
        text='Open Project',
        command=open_window)
button_open.grid(row=1, column=0, padx=10, pady=10)

button_create = Button(button_frame, text="Create Project", command=create_table)
button_create.grid(row=1, column=1, padx=10, pady=10)
button_delete = Button(button_frame, text="Delete Project", command=delete_table)
button_delete.grid(row=1, column=2, padx=10, pady=10)
button_refresh = Button(button_frame, text="Refresh", command=query_database_and_show)
button_refresh.grid(row=1, column=3, padx=10, pady=10)

# resize button text size
def resize(e):
    
    # get window width
    size = e.width//200+10

    style.configure("button_open", font=(None, size))
    # if e.width > 1500:
    fn_label.config(font = ("Helvetica", size))
    fn_entry.config(font = ("Helvetica", size))
    button_frame.config(font = ("Helvetica", size))

    style.configure("Treeview", font=(None, size),rowheight = size+10)
    style.configure("Treeview.Heading", font=(None, size))

root.bind('<Configure>', resize)


root.mainloop()