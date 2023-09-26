from tkinter import ttk
import sqlite3
from window import Window
from tkinter import *
import tkinter as tk



class MainAppWindow(tk.Tk):
    project_name = ''
    def __init__(self, project_name):
        # super().__init__(parent)
        super().__init__()
        # root = self
        # root.title('China Auto CAAS Functional Safety DataBase')
        # root.iconbitmap('D:\Henglong.ico')
        # root.geometry("1100x550")

        self.project_name = project_name

        self.setup_main_window()
        self.setup_treeview()
        self.setup_data_frame()
        self.setup_buttons()
        self.query_database_and_show()
        self.bind('<Configure>', self.resize)

        # root.mainloop()

    def replace_query_tb_name(query:str):
        new_query = query.replace("customers", project_name, 1)
        return new_query
    
    def setup_main_window(self):
        # Setting up the main window geometry
        width = 600
        height = 400
        g_screenwidth = self.winfo_screenwidth()
        g_screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (g_screenwidth - width) / 2, (g_screenheight - height) / 2)
        self.geometry(alignstr)
        self.minsize(width, height)

    def setup_treeview(self):
        # Treeview setup
        self.tree_frame = Frame(self)
        self.tree_frame.pack(fill="both", expand="yes", pady=5, anchor="w", side="top")

        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack(fill="both", expand="yes", padx=5, pady=5, anchor="n", side="top")
        self.tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("Project", "Safety Goal ID", "Safety Goal")
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Project", anchor=W, width=150)
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Project", text="Project", anchor=W)
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

    def setup_data_frame(self):
        # Data frame setup
        self.data_frame = LabelFrame(self, text="")
        self.data_frame.pack(fill="x", expand="yes", padx=20, pady=5, anchor='s')
        self.fn_label = Label(self.data_frame, text="New Project Name")
        self.fn_label.pack(padx=10, pady=5, anchor='w')
        self.fn_entry = Entry(self.data_frame)
        self.fn_entry.pack(fill="x", expand="yes", padx=10, pady=3)

    def query_database_and_show(self):
        # Database query and display
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)

        conn = sqlite3.connect('tree_crm.db')
        c = conn.cursor()

        print("______project name " + self.project_name)
        sql_query = """SELECT * FROM Projects WHERE ProjectName='{}';""".format(self.project_name)

        # sql_query = """SELECT * FROM Projects WHERE ProjectName=customers;""".replace("customers", self.project_name, 1)
        c.execute(sql_query)
        records = c.fetchall()

        print(records)

        count = 0
        for record in records:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[2]),
                            tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[2]),
                            tags=('oddrow',))
            count += 1 

        conn.commit()
        conn.close()

    def open_window(self):
        selected = self.my_tree.focus()
        tb_name = self.my_tree.item(selected)['values'][0]
        print(tb_name)
        window = Window(self, 'tree_crm.db', tb_name)

    # def create_table(self):
    #     conn = sqlite3.connect('tree_crm.db')
    #     c = conn.cursor()

    #     query = """CREATE TABLE if not exists customers (
    #                 id integer,
    #                 address text,
    #                 city text,
    #                 state text,
    #                 zipcode text)
    #                 """
    #     n_query = query.replace("customers", self.fn_entry.get())
    #     c.execute(n_query)

    #     conn.commit()
    #     conn.close()

    #     self.fn_entry.delete(0, END)
    #     self.my_tree.delete(*self.my_tree.get_children())
    #     self.query_database_and_show()
    
    def create_table(self):
        # Fetch the subproject table name from the entry
        subproject_table_name = self.fn_entry.get()

        # Connect to the database
        conn = sqlite3.connect('tree_crm.db')
        c = conn.cursor()

        # Insert the new subproject table name and associated main project name into the Projects table
        c.execute("INSERT INTO Projects (ProjectName, SubProjectTableName) VALUES (?, ?)", (self.project_name, subproject_table_name))

        # Create the new subproject table
        c.execute(f"""CREATE TABLE IF NOT EXISTS {subproject_table_name} (
                        id integer,
                        address text,
                        city text,
                        state text,
                        zipcode text)
                    """)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Clear entry boxes and refresh the treeview
        self.fn_entry.delete(0, END)
        self.query_database_and_show()



    def delete_table(self):
        selected = self.my_tree.focus()
        tb_name = self.my_tree.item(selected)['values'][0]
        conn = sqlite3.connect('tree_crm.db')
        c = conn.cursor()
        c.execute("DROP TABLE {}".format(tb_name))
        conn.commit()
        conn.close()
        self.query_database_and_show()

    def setup_buttons(self):
        self.button_frame = LabelFrame(self, text="Commands")
        self.button_frame.pack(fill="x", expand="yes", padx=20, anchor="s", side="bottom")

        self.button_open = Button(self.button_frame, text='Open Project', command=self.open_window)
        self.button_open.grid(row=1, column=0, padx=10, pady=10)

        self.button_create = Button(self.button_frame, text="Create Project", command=self.create_table)
        self.button_create.grid(row=1, column=1, padx=10, pady=10)

        self.button_delete = Button(self.button_frame, text="Delete Project", command=self.delete_table)
        self.button_delete.grid(row=1, column=2, padx=10, pady=10)

        self.button_refresh = Button(self.button_frame, text="Refresh", command=self.query_database_and_show)
        self.button_refresh.grid(row=1, column=3, padx=10, pady=10)

    def resize(self, e):
        size = e.width // 200 + 10
        style = ttk.Style()
        style.configure("button_open", font=(None, size))
        self.fn_label.config(font=("Helvetica", size))
        self.fn_entry.config(font=("Helvetica", size))
        self.button_frame.config(font=("Helvetica", size))
        style.configure("Treeview", font=(None, size), rowheight=size + 10)
        style.configure("Treeview.Heading", font=(None, size))


if __name__ == '__main__':
    root = Tk()
    app = MainAppWindow(root)
    root.mainloop()
