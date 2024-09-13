from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np

# Función para cargar una imagen
def cargar_imagen1():
    global img1
    archivo = filedialog.askopenfilename(title="Seleccionar imagen")
    img1 = Image.open(archivo)
    img1.thumbnail((250, 250))
    img1_tk = ImageTk.PhotoImage(img1)
    panel_imagen1.configure(image=img1_tk)
    panel_imagen1.image = img1_tk

def cargar_imagen2():
    global img2
    archivo = filedialog.askopenfilename(title="Seleccionar imagen")
    img2 = Image.open(archivo)
    img2.thumbnail((250, 250))
    img2_tk = ImageTk.PhotoImage(img2)
    panel_imagen2.configure(image=img2_tk)
    panel_imagen2.image = img2_tk

# Función para sumar imágenes
def sumar_imagenes():
    img1_np = np.array(img1.convert('RGB'))
    img2_np = np.array(img2.convert('RGB'))
    
    suma = np.clip(img1_np + img2_np, 0, 255)  # Clamping para evitar desbordamientos
    img_resultante = Image.fromarray(suma.astype('uint8'))
    
    img_resultante.thumbnail((250, 250))
    img_resultante_tk = ImageTk.PhotoImage(img_resultante)
    panel_resultante.configure(image=img_resultante_tk)
    panel_resultante.image = img_resultante_tk

# Función para restar imágenes
def restar_imagenes():
    img1_np = np.array(img1.convert('RGB'))
    img2_np = np.array(img2.convert('RGB'))
    
    resta = np.clip(img1_np - img2_np, 0, 255)
    img_resultante = Image.fromarray(resta.astype('uint8'))
    
    img_resultante.thumbnail((250, 250))
    img_resultante_tk = ImageTk.PhotoImage(img_resultante)
    panel_resultante.configure(image=img_resultante_tk)
    panel_resultante.image = img_resultante_tk

# Interfaz gráfica
root = Tk()
root.title("Aritmética de pixeles PDI")

# Cargar imágenes
btn_cargar1 = Button(root, text="Cargar Imagen 1", command=cargar_imagen1)
btn_cargar1.grid(row=0, column=0, padx=10, pady=10)

btn_cargar2 = Button(root, text="Cargar Imagen 2", command=cargar_imagen2)
btn_cargar2.grid(row=0, column=1, padx=10, pady=10)

# Paneles para mostrar imágenes cargadas
panel_imagen1 = Label(root)
panel_imagen1.grid(row=1, column=0, padx=10, pady=10)

panel_imagen2 = Label(root)
panel_imagen2.grid(row=1, column=1, padx=10, pady=10)

# Botones para operaciones
btn_sumar = Button(root, text="Sumar Imágenes", command=sumar_imagenes)
btn_sumar.grid(row=2, column=0, padx=10, pady=10)

btn_restar = Button(root, text="Restar Imágenes", command=restar_imagenes)
btn_restar.grid(row=2, column=1, padx=10, pady=10)

# Panel para mostrar la imagen resultante
panel_resultante = Label(root)
panel_resultante.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()
