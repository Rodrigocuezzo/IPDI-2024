import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Función para cargar la imagen
def cargar_imagen():
    global img_gray, img
    filepath = filedialog.askopenfilename()
    if filepath:
        img = cv2.imread(filepath)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
        mostrar_imagen(img_gray)

# Función para mostrar la imagen en la interfaz
def mostrar_imagen(img):
    img_pil = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    lbl_img.config(image=img_tk)
    lbl_img.image = img_tk

# Función para aplicar el filtro seleccionado
def aplicar_filtro(filtro):
    global img_gray
    if filtro == "Pasa-bajos 3x3":
        kernel = np.ones((3, 3), np.float32) / 9
    elif filtro == "Pasa-bajos Gaussiano 5x5":
        kernel = cv2.getGaussianKernel(5, 1)
        kernel = kernel @ kernel.T
    elif filtro == "Sobel Este":
        kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    else:
        return

    img_filt = cv2.filter2D(img_gray, -1, kernel)
    mostrar_imagen(img_filt)

# Crear la interfaz gráfica
root = Tk()
root.title("Procesamiento de Imágenes")

# Botón para cargar la imagen
btn_cargar = Button(root, text="Cargar Imagen", command=cargar_imagen)
btn_cargar.pack()

# Lista de opciones de filtros
filtros = ["Pasa-bajos 3x3", "Pasa-bajos Gaussiano 5x5", "Sobel Este"]
var_filtro = StringVar(root)
var_filtro.set(filtros[0])

# Menú desplegable para seleccionar filtro
menu_filtros = OptionMenu(root, var_filtro, *filtros)
menu_filtros.pack()

# Botón para aplicar el filtro
btn_aplicar = Button(root, text="Aplicar Filtro", command=lambda: aplicar_filtro(var_filtro.get()))
btn_aplicar.pack()

# Label para mostrar la imagen
lbl_img = Label(root)
lbl_img.pack()

# Iniciar la interfaz
root.mainloop()
