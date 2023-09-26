import os, time
from tkinter import *
from tkinter import ttk
import tkinter as tk

from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from tkinter import scrolledtext
from tkinter import filedialog

class Window(tk.Toplevel):
    db_name = ''
    tb_name = ''
    def __init__(self, parent, db_name, tb_name) -> None:
        super().__init__(parent)
        root = self
        root.title('China Auto CAAS Functional Safety DataBase')
        # root.iconbitmap('D:\Henglong.ico')
        root.geometry("1100x550")
        self.db_name = db_name
        self.tb_name = tb_name

        def replace_query_tb_name(query:str):
            new_query = query.replace("customers", tb_name, 1)
            return new_query
            
        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            # Create a database or connect to one that exists
            conn = sqlite3.connect(self.db_name)

            # Create a cursor instance
            c = conn.cursor()

            c.execute(replace_query_tb_name("SELECT rowid, * FROM customers"))
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            # for record in records:
            #	print(record)

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='',
                                values=(record[1], record[2], record[3], record[4], record[5]),
                                tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='',
                                values=(record[1], record[2], record[3], record[4], record[5]),
                                tags=('oddrow',))
                # increment counter
                count += 1 

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()


        def search_records():
            lookup_record = search_entry.get()
            # close the search box
            search.destroy()

            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            # Create a database or connect to one that exists
            conn = sqlite3.connect(self.db_name)

            # Create a cursor instance
            c = conn.cursor()

            # c.execute(replace_query_tb_name("SELECT rowid, * FROM customers WHERE id like ?"), (lookup_record,))
            c.execute(replace_query_tb_name("SELECT rowid, * FROM customers WHERE address like '%" + lookup_record +"%'"))
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            # for record in records:
            #	print(record)

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='',
                                values=(record[1], record[2], record[3], record[4], record[5]),
                                tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='',
                                values=(record[1], record[2], record[3], record[4], record[5]),
                                tags=('oddrow',))
                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()


        def lookup_records():
            global search_entry, search

            search = Toplevel(root)
            search.title("Lookup file")
            search.geometry("400x200")
            # search.iconbitmap('D:\Henglong.ico')

            # Create label frame
            search_frame = LabelFrame(search, text="file name")
            search_frame.pack(padx=10, pady=10)

            # Add entry box
            search_entry = Entry(search_frame, font=("Helvetica", 18))
            search_entry.pack(pady=20, padx=20)

            # Add button
            search_button = Button(search, text="Search file", command=search_records)
            search_button.pack(padx=20, pady=20)


        def primary_color():
            # Pick Color
            primary_color = colorchooser.askcolor()[1]

            # Update Treeview Color
            if primary_color:
                # Create Striped Row Tags
                my_tree.tag_configure('evenrow', background=primary_color)


        def secondary_color():
            # Pick Color
            secondary_color = colorchooser.askcolor()[1]

            # Update Treeview Color
            if secondary_color:
                # Create Striped Row Tags
                my_tree.tag_configure('oddrow', background=secondary_color)


        def highlight_color():
            # Pick Color
            highlight_color = colorchooser.askcolor()[1]

            # Update Treeview Color
            # Change Selected Color
            if highlight_color:
                style.map('Treeview',
                        background=[('selected', highlight_color)])


        # Add Menu
        my_menu = Menu(root)
        root.config(menu=my_menu)

        # Configure our menu
        option_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Options", menu=option_menu)
        # Drop down menu
        option_menu.add_command(label="Primary Color", command=primary_color)
        option_menu.add_command(label="Secondary Color", command=secondary_color)
        option_menu.add_command(label="Highlight Color", command=highlight_color)
        option_menu.add_separator()
        option_menu.add_command(label="Exit", command=root.quit)

        # Search Menu
        search_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Search", menu=search_menu)
        # Drop down menu
        search_menu.add_command(label="Search", command=lookup_records)
        search_menu.add_separator()
        search_menu.add_command(label="Refresh", command=query_database)

        # Add Fake Data
        # '''
        # data = [
        #     ["John", "Elder", 1, "123 Elder St.", "Las Vegas", "NV", "89137"],
        #     ["Mary", "Smith", 2, "435 West Lookout", "Chicago", "IL", "60610"],
        #     ["Tim", "Tanaka", 3, "246 Main St.", "New York", "NY", "12345"],
        #     ["Erin", "Erinton", 4, "333 Top Way.", "Los Angeles", "CA", "90210"],
        #     ["Bob", "Bobberly", 5, "876 Left St.", "Memphis", "TN", "34321"],
        #     ["Steve", "Smith", 6, "1234 Main St.", "Miami", "FL", "12321"],
        #     ["Tina", "Browne", 7, "654 Street Ave.", "Chicago", "IL", "60611"],
        #     ["Mark", "Lane", 8, "12 East St.", "Nashville", "TN", "54345"],
        #     ["John", "Smith", 9, "678 North Ave.", "St. Louis", "MO", "67821"],
        #     ["Mary", "Todd", 10, "9 Elder Way.", "Dallas", "TX", "88948"],
        #     ["John", "Lincoln", 11, "123 Elder St.", "Las Vegas", "NV", "89137"],
        #     ["Mary", "Bush", 12, "435 West Lookout", "Chicago", "IL", "60610"],
        #     ["Tim", "Reagan", 13, "246 Main St.", "New York", "NY", "12345"],
        #     ["Erin", "Smith", 14, "333 Top Way.", "Los Angeles", "CA", "90210"],
        #     ["Bob", "Field", 15, "876 Left St.", "Memphis", "TN", "34321"],
        #     ["Steve", "Target", 16, "1234 Main St.", "Miami", "FL", "12321"],
        #     ["Tina", "Walton", 17, "654 Street Ave.", "Chicago", "IL", "60611"],
        #     ["Mark", "Erendale", 18, "12 East St.", "Nashville", "TN", "54345"],
        #     ["John", "Nowerton", 19, "678 North Ave.", "St. Louis", "MO", "67821"],
        #     ["Mary", "Hornblower", 20, "9 Elder Way.", "Dallas", "TX", "88948"]

        # ]
        # '''

        # Do some database stuff
        # Create a database or connect to one that exists
        conn = sqlite3.connect(self.db_name)

        # Create a cursor instance
        c = conn.cursor()

        # Create Table
        c.execute(replace_query_tb_name("""CREATE TABLE if not exists customers (
            id integer primary key,
            address text,
            city text,
            state text,
            zipcode text)
            """))
        # Add dummy data to table
        '''
        for record in data:
            c.execute("INSERT INTO customers VALUES (:id, :address, :city, :state, :zipcode)", 
                {
                'id': record[0],
                'address': record[1],
                'city': record[2],
                'state': record[3],
                'zipcode': record[4]
                }
                )
        '''

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")

        # Change Selected Color
        style.map('Treeview',
                background=[('selected', "#347083")])

        # Create a Treeview Frame
        tree_frame = Frame(root)
        tree_frame.pack(fill="both",expand="yes",pady=5,anchor = "w", side = "top")

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack(fill="both",expand="yes",padx = 5 ,pady=5,anchor = "n", side = "top")

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "File Name", "Version", "Date", "Directory")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=CENTER, width=50)
        my_tree.column("File Name", anchor=CENTER, width=250)
        my_tree.column("Version", anchor=CENTER, width=50)
        my_tree.column("Date", anchor=CENTER, width=80)
        my_tree.column("Directory", anchor=CENTER, width=400)

        # Create Headings
        my_tree.heading("ID", text="ID", anchor=CENTER)
        my_tree.heading("File Name", text="File Name", anchor=CENTER)
        my_tree.heading("Version", text="Version", anchor=CENTER)
        my_tree.heading("Date", text="Date", anchor=CENTER)
        my_tree.heading("Directory", text="Directory", anchor=CENTER)

        # Create Striped Row Tags
        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="lightblue")

        # Add Record Entry Boxes
        data_frame = LabelFrame(root, text="Requirement")
        data_frame.pack(fill="x", expand="yes", padx=20)
        entry_frame = LabelFrame(root, text="Requirement Content")
        entry_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=4, padx=8, pady=8)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=5, padx=8, pady=8)

        address_label = Label(entry_frame, text="File Name")
        address_label.grid(row=0, column=0, padx=8, pady=8)
        address_entry = Entry(entry_frame,width = 100)
        address_entry.grid(row=0, column=1, padx=8, pady=8)

        city_label = Label(data_frame, text="Version")
        city_label.grid(row=0, column=6, padx=8, pady=8)
        city_entry = Entry(data_frame)
        city_entry.grid(row=0, column=7, padx=8, pady=8)

        state_label = Label(data_frame, text="Date")
        state_label.grid(row=0, column=8, padx=8, pady=8)
        state_entry = Entry(data_frame)
        state_entry.grid(row=0, column=9, padx=8, pady=8)

        zipcode_label = Label(entry_frame, text="Directory")
        zipcode_label.grid(row=1, column=0, padx=8, pady=8)
        #zipcode_entry = scrolledtext.ScrolledText(entry_frame, wrap=tk.WORD,
        #                              width=100, height=8)
        zipcode_entry = Entry(entry_frame,width = 100)
        zipcode_entry.grid(row=1, column=1, padx=8, pady=8)



        def browseFiles():
            filename = filedialog.askopenfilename(initialdir = "/",
                                                title = "Select a File",
                                                filetypes = (
                                                            ("all files",
                                                                "*.*"),("Excel files",
                                                                "*.xlxs*")))
            (path,name) = os.path.split(filename)
            modify_time = time.localtime(os.stat(filename).st_mtime)
            mtime = time.strftime("%m/%d/%Y",modify_time)
            conn = sqlite3.connect('tree_crm.db')
            c = conn.cursor()
            c.execute(replace_query_tb_name("SELECT rowid, * FROM customers"))
            records = c.fetchall()
            newid = len(records) + 1
            # Change label contents
            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()
            zipcode_entry.insert(0, filename)            
            id_entry.insert(0, newid)
            address_entry.insert(0,name)
            state_entry.insert(0,mtime)

        def OnDoubleClick(self):
            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')
            filename = values[4]
            diretory = r'"{}"'.format(filename)
            os.system(diretory)
        my_tree.bind("<Double-1>", OnDoubleClick)

        
        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)


        # Move Rown Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)


        # Remove one record
        def remove_one():
            x = my_tree.selection()[0]
            my_tree.delete(x)

            # Create a database or connect to one that exists
            conn = sqlite3.connect(self.db_name)

            # Create a cursor instance
            c = conn.cursor()

            # Delete From Database
            c.execute(replace_query_tb_name("""DELETE FROM customers WHERE ID = :id"""),{'id': id_entry.get()})

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()
            query_database()

            # Add a little message box for fun
            messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")


        # Remove Many records
        def remove_many():
            # Add a little message box for fun
            response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

            # Add logic for message box
            if response == 1:
                # Designate selections
                x = my_tree.selection()

                # Create List of ID's
                ids_to_delete = []

                # Add selections to ids_to_delete list
                for record in x:
                    ids_to_delete.append(my_tree.item(record, 'values')[0])

                # Delete From Treeview
                for record in x:
                    my_tree.delete(record)

                # Create a database or connect to one that exists
                conn = sqlite3.connect(self.db_name)

                # Create a cursor instance
                c = conn.cursor()

                # Delete Everything From The Table
                c.executemany(replace_query_tb_name("""DELETE FROM customers WHERE ID = :id"""),{'id': (a,) for a in ids_to_delete})

                # Reset List
                ids_to_delete = []

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes if filled
                clear_entries()
                query_database()


        # Remove all records
        def remove_all():
            # Add a little message box for fun
            response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                # Create a database or connect to one that exists
                conn = sqlite3.connect(self.db_name)

                # Create a cursor instance
                c = conn.cursor()

                # Delete Everything From The Table
                c.execute(replace_query_tb_name("DROP TABLE customers"))

                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes if filled
                clear_entries()

                # Recreate The Table
                create_table_again()
                query_database()


        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            address_entry.delete(0, END)
            city_entry.delete(0, END)
            state_entry.delete(0, END)
            zipcode_entry.delete(0, END)


        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            address_entry.delete(0, END)
            city_entry.delete(0, END)
            state_entry.delete(0, END)
            zipcode_entry.delete(0, END)

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')

            # outpus to entry boxes
            id_entry.insert(0, values[0])
            address_entry.insert(0, values[1])
            city_entry.insert(0, values[2])
            state_entry.insert(0, values[3])
            zipcode_entry.insert(0, values[4])


        # Update record
        def update_record():
            # Grab the record number
            selected = my_tree.focus()
            # Update record
            my_tree.item(selected, text="", values=(
            id_entry.get(), address_entry.get(), city_entry.get(), state_entry.get(),
            zipcode_entry.get(),))

            # Update the database
            # Create a database or connect to one that exists
            conn = sqlite3.connect(self.db_name)

            # Create a cursor instance
            c = conn.cursor()

            c.execute(replace_query_tb_name("""UPDATE customers SET
                address = :address,
                city = :city,
                state = :state,
                zipcode = :zipcode

                WHERE id = :id"""),
                    {
                        'address': address_entry.get(),
                        'city': city_entry.get(),
                        'state': state_entry.get(),
                        'zipcode': zipcode_entry.get(),
                        'id': id_entry.get(),
                    })

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear entry boxes
            id_entry.delete(0, END)
            address_entry.delete(0, END)
            city_entry.delete(0, END)
            state_entry.delete(0, END)
            zipcode_entry.delete(0, END)
            query_database()


        # add new record to database
        def add_record():
            # Update the database
            # Create a database or connect to one that exists
            conn = sqlite3.connect(self.db_name)


            # Create a cursor instance
            c = conn.cursor()

            # Add New Record
            c.execute(replace_query_tb_name("INSERT OR IGNORE INTO customers VALUES (:id, :address, :city, :state, :zipcode)"),
                    {
                        'id': id_entry.get(),
                        'address': address_entry.get(),
                        'city': city_entry.get(),
                        'state': state_entry.get(),
                        'zipcode': zipcode_entry.get(),
                    })

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear entry boxes
            id_entry.delete(0, END)
            address_entry.delete(0, END)
            city_entry.delete(0, END)
            state_entry.delete(0, END)
            zipcode_entry.delete(0, END)

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()


        def create_table_again():
            # Create a database or connect to one that exists
            conn = sqlite3.connect(self.db_name)

            # Create a cursor instance
            c = conn.cursor()

            # Create Table
            c.execute(replace_query_tb_name("""CREATE TABLE if not exists customers (
                id integer,
                address text,
                city text,
                state text,
                zipcode text)
                """))

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()


        # Add Buttons
        button_frame = LabelFrame(root, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        button_explore = Button(button_frame, text = "Browse Files", command = browseFiles)
        button_explore.grid(row=0, column=0, padx=10, pady=10)

        add_button = Button(button_frame, text="Add File", command=add_record)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        update_button = Button(button_frame, text="Update File", command=update_record)
        update_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
        remove_one_button.grid(row=0, column=4, padx=10, pady=10)

        # remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
        # remove_many_button.grid(row=0, column=4, padx=10, pady=10)

        # move_up_button = Button(button_frame, text="Move Up", command=up)
        # move_up_button.grid(row=1, column=0, padx=10, pady=10)

        # move_down_button = Button(button_frame, text="Move Down", command=down)
        # move_down_button.grid(row=1, column=1, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=5, padx=10, pady=10)

        search_record_button = Button(button_frame, text="Search", command=lookup_records)
        search_record_button.grid(row=0, column=6, padx=10, pady=10)



        button_refresh = Button(button_frame, text="Refresh", command=query_database())
        button_refresh.grid(row=0, column=7, padx=10, pady=10)


        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()

        root.mainloop()