from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import csv
import os
from tkinter import filedialog
from tkinter import messagebox
import sqlite3



class Stock:
 # propiedades de la conexion a base de datos---
    db_name = 'tree_crm.db'

def __init__(self, window):

    # Inicializacion
    self.Ventana_Principal = window
    self.Ventana_Principal.title('Software Prueba')

    # Contenedor de Entrada de datos
    frame = LabelFrame(self.Ventana_Principal, text = 'Productos--')
    frame.grid(row = 0, column = 0, columnspan = 30, padx = 30, pady = 30)

    # Entrada de Clave
    Label(frame, text = 'Clave: ').grid(row = 1, column = 0)
    self.Clave = Entry(frame)
    self.Clave.focus()
    self.Clave.grid(row = 1, column = 1)

    # Entrada de Unidad
    Label(frame, text = 'Unidad: ').grid(row = 2, column = 0)
    self.Unidad = Entry(frame)
    self.Unidad.grid(row = 2, column = 1)

    # Entrada de Nombre Producto
    Label(frame, text = 'Nombre: ').grid(row = 3, column = 0)
    self.Nombre = Entry(frame)
    self.Nombre.grid(row = 3, column = 1)

    # Entrada de Cantidad
    Label(frame, text = 'Cantidad: ').grid(row = 1, column = 2)
    self.Cantidad = Entry(frame)
    self.Cantidad.grid(row = 1, column = 3)

    # Entrada de Precio Compra
    Label(frame, text = 'Precio Compra: ').grid(row = 2, column = 2)
    self.PrecioCompra = Entry(frame)
    self.PrecioCompra.grid(row = 2, column = 3)

    # Entrada de Precio Venta
    Label(frame, text = 'Precio Venta: ').grid(row = 3, column = 2)
    self.PrecioVenta = Entry(frame)
    self.PrecioVenta.grid(row = 3, column = 3)


    # Boton Agregar Producto - Importar Archivo
    ttk.Button(frame, text = 'Guardar Producto', command = self.agregar_productos).grid(row = 10, columnspan = 5, sticky = W + E)


    #Seccion de Busqueda
    Label(frame, text = 'Buscar: ').grid(row = 4, column = 0)
    self.Buscador = Entry(frame, textvariable = StringVar())
    self.Buscador.grid(row = 4, column = 1)
    Button(frame, text = "Buscar Producto", command = self.buscar_registro).grid(row = 4, column = 2)


    # Mensajes de Salida
    self.mensaje = Label(text = '', fg = 'red')
    self.mensaje.grid(row = 3, column = 5, columnspan = 5, sticky = W + E)

    # Tabla
    self.tabla = ttk.Treeview(height = 10, columns = ('#1','#2','#3','#4'))
    self.tabla.grid(row = 4, column = 5, columnspan = 5)
    self.tabla.heading('#0', text = 'Codigo/Clave', anchor = CENTER)
    self.tabla.heading('#1', text = 'Producto', anchor = CENTER)
    self.tabla.heading('#2', text = 'Cantidad', anchor = CENTER)
    self.tabla.heading('#3', text = 'Precio Compra', anchor = CENTER)
    self.tabla.heading('#4', text = 'Precio Venta', anchor = CENTER)

    # Botones Eliminar - Editar - Importar
    ttk.Button(text = 'Editar', command = self.editar_productos).grid(row = 5, column = 5, sticky = W + E)
    ttk.Button(text = 'Eliminar', command = self.eliminar_productos).grid(row = 5, column = 9, sticky = W + E)
    ttk.Button(text = 'Importar Archivo', command = self.importar_csv).grid(row = 1, column = 7, sticky = W + E)
    ttk.Button(text = 'Exportar Archivo', command = self.exportar_csv).grid(row = 2, column = 7, sticky = W + E)

    # Ordenando las filas
    self.ordenar_productos()

# Funcion a ejecutar en la base de datos --Querys--
def run_query(self, query, parameters = ()):
    with sqlite3.connect(self.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

# Leer Tabla de base de datos
def ordenar_productos(self):
    # Limpiar Tabla
    records = self.tabla.get_children()
    for element in records:
        self.tabla.delete(element)
    # Seleccionar datos
    query = 'SELECT * FROM Productos ORDER BY Clave DESC'
    db_rows = self.run_query(query)
    # Acomodar datos
    for row in db_rows:
        self.tabla.insert('', 0, text = row[1], values = row[3:7])


def buscar_registro(self):
    self.buscar = self.Buscador.get()
    query = "SELECT Nombre FROM Productos WHERE Nombre LIKE ? ORDER BY Nombre DESC"
    self.run_query(query, ('%' + self.buscar + '%',))   #"SELECT Nombre FROM Productos WHERE Nombre LIKE '%"+self.Buscador.get()+"%' ORDER BY Nombre DESC"
    parameters = (self.buscar)
    self.run_query(query, parameters)
    self.ordenar_productos()

    #palabra = self.Buscador.get()
    #query = "SELECT Nombre FROM Productos WHERE Nombre LIKE '%"+self.buscar+"%' ORDER BY Nombre DESC"
    #parameters = (self.buscar)
    #self.run_query(query, parameters).fetchall()
    #self.ordenar_productos()



# Validacion de datos ingresados por el usuario
def validacion(self):
    return len(self.Clave.get()) != 0 and len(self.Nombre.get()) != 0 and len(self.Cantidad.get()) != 0 and len(self.PrecioCompra.get()) != 0 and len(self.PrecioVenta.get()) != 0

# Funcion Agregar Productos
def agregar_productos(self):
    if self.validacion():
        query = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?, ?, ?, ?)'
        parameters =  (self.Clave.get(), self.Unidad.get(), self.Nombre.get(), self.Cantidad.get(), self.PrecioCompra.get(), self.PrecioVenta.get())
        self.run_query(query, parameters)
        self.mensaje['text'] = 'Producto {} Se Agrego Correctamente'.format(self.Nombre.get())
        self.Clave.delete(0, END)
        self.Unidad.delete(0, END)
        self.Nombre.delete(0, END)
        self.Cantidad.delete(0, END)
        self.PrecioCompra.delete(0, END)
        self.PrecioVenta.delete(0, END)
    else:
        self.mensaje['text'] = 'Los Campos no Pueden estar Vacios'
    self.ordenar_productos()

# Funcion de Eliminar
def eliminar_productos(self):
    self.mensaje['text'] = ''
    try:
       self.tabla.item(self.tabla.selection())['values'][0]
    except IndexError as e:
        self.mensaje['text'] = 'Debe Seleccionar un Registro'
        return
    self.mensaje['text'] = ''
    nombre = self.tabla.item(self.tabla.selection())['text']
    query = 'DELETE FROM Productos WHERE Clave = ?'
    self.run_query(query, (nombre, ))
    self.mensaje['text'] = 'Registro {} Eliminado'.format(nombre)
    self.ordenar_productos()


# Funcion de Edicion
def editar_productos(self):
    self.mensaje['text'] = ''
    try:
        self.tabla.item(self.tabla.selection())['values'][0]
    except IndexError as e:
        self.mensaje['text'] = 'Debe Seleccionar un Registro'
        return
    Nombre_Anterior = self.tabla.item(self.tabla.selection())['values'][0]
    Cantidad_Anterior = self.tabla.item(self.tabla.selection())['values'][1]
    Precio_Anterior_Compra = self.tabla.item(self.tabla.selection())['values'][2]
    Precio_Anterior_Venta = self.tabla.item(self.tabla.selection())['values'][3]
    self.Ventana_Edicion = Toplevel()
    self.Ventana_Edicion.title ('Editar Producto')

    # Nombre Anterior
    Label(self.Ventana_Edicion, text = 'Nombre Anterior:').grid(row = 0, column = 1)
    Entry(self.Ventana_Edicion, textvariable = StringVar(self.Ventana_Edicion, value = Nombre_Anterior), state = 'readonly').grid(row = 0, column = 2)

    # Nuevo Nombre
    Label(self.Ventana_Edicion, text = 'Nuevo Nombre:').grid(row = 1, column = 1)
    Nuevo_Nombre = Entry(self.Ventana_Edicion)
    Nuevo_Nombre.grid(row = 1, column = 2)

     # Cantidad Anterior
    Label(self.Ventana_Edicion, text = 'Stock Anterior:').grid(row = 2, column = 1)
    Entry(self.Ventana_Edicion, textvariable = StringVar(self.Ventana_Edicion, value = Cantidad_Anterior), state = 'readonly').grid(row = 2, column = 2)

    # Nueva Cantidad
    Label(self.Ventana_Edicion, text = 'Nuevo Stock:').grid(row = 3, column = 1)
    Nueva_Cantidad= Entry(self.Ventana_Edicion)
    Nueva_Cantidad.grid(row = 3, column = 2)

    # Precio Compra Anterior
    Label(self.Ventana_Edicion, text = 'Precio Compra Anterior :').grid(row = 0, column = 3)
    Entry(self.Ventana_Edicion, textvariable = StringVar(self.Ventana_Edicion, value = Precio_Anterior_Compra), state = 'readonly').grid(row = 0, column = 4)

    # Nuevo Precio de Compra
    Label(self.Ventana_Edicion, text = 'Nuevo Precio Compra:').grid(row = 1, column = 3)
    Nuevo_Precio_Compra= Entry(self.Ventana_Edicion)
    Nuevo_Precio_Compra.grid(row = 1, column = 4)

    # Precio Venta Anterior
    Label(self.Ventana_Edicion, text = 'Precio Venta Anterior:').grid(row = 2, column = 3)
    Entry(self.Ventana_Edicion, textvariable = StringVar(self.Ventana_Edicion, value = Precio_Anterior_Venta), state = 'readonly').grid(row = 2, column = 4)

    # Nuevo Precio de Venta
    Label(self.Ventana_Edicion, text = 'Nuevo Precio Venta:').grid(row = 3, column = 3)
    Nuevo_Precio_Venta= Entry(self.Ventana_Edicion)
    Nuevo_Precio_Venta.grid(row = 3, column = 4)

    # Boton Actualizar
    Button(self.Ventana_Edicion, text = 'Actualizar', command = lambda: self.editar_registros(Nuevo_Nombre.get(), Nombre_Anterior, Nueva_Cantidad.get(), Cantidad_Anterior, Nuevo_Precio_Compra.get(), Precio_Anterior_Compra, Nuevo_Precio_Venta.get(), Precio_Anterior_Venta)).grid(row = 8, columnspan = 5, sticky = W + E)
    self.Ventana_Edicion.mainloop()

# funcion de edicion
def editar_registros(self, Nuevo_Nombre, Nombre_Anterior, Nueva_Cantidad, Cantidad_Anterior, Nuevo_Precio_Compra, Precio_Anterior_Compra, Nuevo_Precio_Venta, Precio_Anterior_Venta):
    query = 'UPDATE Productos SET Nombre = ?, Cantidad = ?, PrecioCompra = ?, PrecioVenta = ? WHERE Nombre = ? AND Cantidad = ? AND PrecioCompra = ? AND PrecioVenta = ?'
    parameters = (Nuevo_Nombre, Nueva_Cantidad, Nuevo_Precio_Compra, Nuevo_Precio_Venta, Nombre_Anterior, Cantidad_Anterior, Precio_Anterior_Compra, Precio_Anterior_Venta)
    self.run_query(query, parameters)
    self.Ventana_Edicion.destroy()
    self.mensaje['text'] = 'Registro {} fue Actualizado Correctamente'.format(Nuevo_Nombre)
    self.ordenar_productos()



if __name__ == '__main__':
    window = Tk()
    application = Stock(window)
    window.mainloop()