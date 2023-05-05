import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import pandas as pd
from openpyxl import Workbook
datos_mostrados = []

def mostrar_datos(datos):
    item_frame = tk.Frame(items_frame, padx=10, pady=10)

    # Verificar si los datos ya existen en la lista
    repetido = datos_mostrados.count(datos) > 0

    # Establecer el color del marco según si el item es repetido o no
    if repetido:
        item_frame.configure(bg="#ffdddd")  # Rojo suave
    else:
        item_frame.configure(bg="white")

    item_frame.pack(pady=10, fill=tk.X)

    label_datos = tk.Label(item_frame, text=datos)
    label_datos.pack(side=tk.LEFT)

    def eliminar_item():
        item_frame.destroy()
        # Remover los datos de la lista cuando se elimina el item
        datos_mostrados.remove(datos)
        buscar_items_repetidos()

    boton_eliminar = tk.Button(item_frame, text="Quitar", command=eliminar_item)
    boton_eliminar.pack(side=tk.RIGHT)

    # Actualizar la lista de datos mostrados
    datos_mostrados.append(datos)
    buscar_items_repetidos()

""" def buscar_items_repetidos():
    for widget in columna2.winfo_children():
        if isinstance(widget, tk.Frame):
            label = widget.winfo_children()[0]
            datos = label["text"]
            repetido = datos_mostrados.count(datos) > 1
            if repetido:
                widget.configure(bg="#ffdddd")  # Rojo suave
            else:
                widget.configure(bg="white")
    
    # Verificar si hay elementos repetidos en rojo
    elementos_repetidos = any(datos_mostrados.count(datos) > 1 for datos in datos_mostrados)
    if not elementos_repetidos:
        mostrar_boton_generar_excel()
    else:
        ocultar_boton_generar_excel() """
def buscar_items_repetidos():
    for widget in items_frame.winfo_children():  # Cambiar columna2 por items_frame
        if isinstance(widget, tk.Frame):
            label = widget.winfo_children()[0]
            datos = label["text"]
            repetido = datos_mostrados.count(datos) > 1
            if repetido:
                widget.configure(bg="#ffdddd")  # Rojo suave
            else:
                widget.configure(bg="white")

    # Verificar si hay elementos repetidos en rojo
    elementos_repetidos = any(datos_mostrados.count(datos) > 1 for datos in datos_mostrados)
    if not elementos_repetidos:
        mostrar_boton_generar_excel()
    else:
        ocultar_boton_generar_excel()

    items_frame.update_idletasks()  # Actualizar tamaño del items_frame
    columna2.configure(scrollregion=columna2.bbox("all"))  # Configurar scrollregion

def mostrar_boton_generar_excel():
    boton_generar_excel.pack(pady=10)

def ocultar_boton_generar_excel():
    boton_generar_excel.pack_forget()

def obtener_datos_xml():
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos XML", "*.xml")])
    if archivos:
        for archivo in archivos:
            with open(archivo, 'r') as file:
                xml_string = file.read()

            root = ET.fromstring(xml_string)

            emisor1 = root.find('.//{http://www.sat.gob.mx/cfd/3}Emisor')
            emisor2 = root.find('.//{http://www.sat.gob.mx/cfd/4}Emisor')

            if emisor1 is not None:
                emisor = emisor1
            elif emisor2 is not None:
                emisor = emisor2
            else:
                emisor = None

            receptor1 = root.find('.//{http://www.sat.gob.mx/cfd/3}Receptor')
            receptor2 = root.find('.//{http://www.sat.gob.mx/cfd/4}Receptor')

            if receptor1 is not None:
                receptor = receptor1
            elif receptor2 is not None:
                receptor = receptor2
            else:
                receptor = None

            nombre_emisor = emisor.attrib.get('Nombre', '')
            rfc_emisor = emisor.attrib.get('Rfc', '')
            nombre_receptor = receptor.attrib.get('Nombre', '')
            rfc_receptor = receptor.attrib.get('Rfc', '')

            datos = f"Archivo: {archivo}\n" \
                    f"Nombre del Emisor: {nombre_emisor}\n" \
                    f"RFC del Emisor: {rfc_emisor}\n" \
                    f"Nombre del Receptor: {nombre_receptor}\n" \
                    f"RFC del Receptor: {rfc_receptor}\n\n"

            mostrar_datos(datos)
    else:
        mostrar_datos("No se seleccionaron archivos XML")

def agregar_mas_xml():
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos XML", "*.xml")])
    if archivos:
        for archivo in archivos:
            with open(archivo, 'r') as file:
                xml_string = file.read()

            root = ET.fromstring(xml_string)

            emisor1 = root.find('.//{http://www.sat.gob.mx/cfd/3}Emisor')
            emisor2 = root.find('.//{http://www.sat.gob.mx/cfd/4}Emisor')

            if emisor1 is not None:
                emisor = emisor1
            elif emisor2 is not None:
                emisor = emisor2
            else:
                emisor = None

            receptor1 = root.find('.//{http://www.sat.gob.mx/cfd/3}Receptor')
            receptor2 = root.find('.//{http://www.sat.gob.mx/cfd/4}Receptor')

            if receptor1 is not None:
                receptor = receptor1
            elif receptor2 is not None:
                receptor = receptor2
            else:
                receptor = None

            nombre_emisor = emisor.attrib.get('Nombre', '')
            rfc_emisor = emisor.attrib.get('Rfc', '')
            nombre_receptor = receptor.attrib.get('Nombre', '')
            rfc_receptor = receptor.attrib.get('Rfc', '')

            datos = f"Archivo: {archivo}\n" \
                    f"Nombre del Emisor: {nombre_emisor}\n" \
                    f"RFC del Emisor: {rfc_emisor}\n" \
                    f"Nombre del Receptor: {nombre_receptor}\n" \
                    f"RFC del Receptor: {rfc_receptor}\n\n"

            mostrar_datos(datos)
    else:
        mostrar_datos("No se seleccionaron archivos XML")
def generar_excel():
    # Verificar si hay datos para generar el Excel
    if len(datos_mostrados) == 0:
        return

    # Crear una lista para almacenar los datos
    datos_excel = []

    # Extraer los datos de cada item y agregarlos a la lista
    for datos in datos_mostrados:
        archivo, nombre_emisor, rfc_emisor, nombre_receptor, rfc_receptor = datos.split("\n")[0:5]
        datos_excel.append([archivo.split(": ")[1], nombre_emisor.split(": ")[1], rfc_emisor.split(": ")[1],
                            nombre_receptor.split(": ")[1], rfc_receptor.split(": ")[1]])

    # Crear un DataFrame a partir de la lista de datos
    df = pd.DataFrame(datos_excel, columns=["Archivo", "nombre_emisor", "rfc_emisor", "nombre_receptor", "rfc_receptor"])

    # Crear el archivo de Excel
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                  filetypes=[("Archivos de Excel", "*.xlsx")])

    if nombre_archivo:
        df.to_excel(nombre_archivo, index=False)
        print(f"Se generó el archivo '{nombre_archivo}' correctamente.")
    else:
        print("No se seleccionó ningún archivo de destino.")

root = tk.Tk()
root.geometry("900x400")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=5)

columna1 = tk.Frame(root)
columna1.grid(row=0, column=0)

cuadrado = tk.Frame(columna1, width=100, height=100, padx=50, pady=50)
cuadrado.pack(fill=tk.BOTH, expand=True)

label = tk.Label(cuadrado, text="Prototype 1. 4/5/2023 hora 10:26")
label.pack(pady=20, padx=50)

boton = tk.Button(cuadrado, text="Agrega XML", command=obtener_datos_xml)
boton.config(width=15, height=3)
boton.pack(pady=20, padx=50)

columna2 = tk.Canvas(root, bg="grey")
columna2.grid(row=0, column=1, sticky="nsew")
scrollbar = ttk.Scrollbar(columna2, orient="vertical", command=columna2.yview)
scrollbar.pack(side="right", fill="y")

columna2.configure(yscrollcommand=scrollbar.set)
items_frame = tk.Frame(columna2, bg="grey")
columna2.create_window((0, 0), window=items_frame, anchor="nw")


def limpiar_items():
    for widget in columna2.winfo_children():
        widget.destroy()
    datos_mostrados.clear()
    ocultar_boton_generar_excel()

boton_limpiar = tk.Button(columna2, text="Limpiar", command=limpiar_items)
boton_limpiar.pack(pady=10)

boton_agregar = tk.Button(columna2, text="Agregar más XML", command=agregar_mas_xml)
boton_agregar.pack(pady=10)

boton_generar_excel = tk.Button(cuadrado, text="Generar Excel", bg="green", fg="white", command=generar_excel)

def mostrar_boton_generar_excel():
    boton_generar_excel.pack(pady=10)

def ocultar_boton_generar_excel():
    boton_generar_excel.pack_forget()

root.mainloop()