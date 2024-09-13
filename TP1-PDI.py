import tkinter as tk
from tkinter import filedialog, StringVar, OptionMenu, simpledialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
import imageio.v3 as iio
import numpy as np

# Variables globales asiganadas
rutaImagen = None
canvasOriginal = None
canvasProcesado = None

#funciones de procesamineto
def procesarBlancoNegro(imagen):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.imshow(imagen[:, :, 0], cmap='gray')
    ax.set_title("Blanco y Negro")
    ax.axis('off')
    return fig

def procesarCanal(imagen, canal, titulo, cmap):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.imshow(imagen[:, :, canal], cmap=cmap)
    ax.set_title(titulo)
    ax.axis('off')
    return fig

def procesarCanalesRGB(imagen):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    canales = [("Rojo", 'Reds', 0), ("Verde", 'Greens', 1), ("Azul", 'Blues', 2)]
    for ax, (titulo, cmap, canal) in zip(axs, canales):
        ax.imshow(imagen[:, :, canal], cmap=cmap)
        ax.set_title(f"Canal {titulo}")
        ax.axis('off')
    return fig

def procesarLuminanciaSaturacion(imagen, a, b):
    fig = plt.figure(figsize=(6, 4))
    gs = GridSpec(3, 4, figure=fig)

    yiq = np.zeros(imagen.shape)
    yiq[:, :, 0] = np.clip(0.299 * imagen[:, :, 0] + 0.587 * imagen[:, :, 1] + 0.114 * imagen[:, :, 2], 0, 1)
    yiq[:, :, 1] = np.clip(0.59 * imagen[:, :, 0] - 0.27 * imagen[:, :, 1] - 0.32 * imagen[:, :, 2], -0.5957, 0.5957)
    yiq[:, :, 2] = np.clip(0.21 * imagen[:, :, 0] - 0.52 * imagen[:, :, 1] + 0.31 * imagen[:, :, 2], -0.5226, 0.5226)

    # Subplot de imagen YIQ
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(yiq)
    ax1.set_title("YIQ")
    ax1.axis('off')

    # Canales YIQ individuales
    canales = [("Y", 0), ("I", 1), ("Q", 2)]
    for i, (titulo, canal) in enumerate(canales):
        ax = fig.add_subplot(gs[0, i+1])
        ax.imshow(yiq[:, :, canal], cmap='gray')
        ax.set_title(f"Canal {titulo}")
        ax.axis('off')

    # Procesar y mostrar imagen resultante
    y1 = np.clip(a * yiq[:, :, 0], 0, 1)
    i2 = np.clip(b * yiq[:, :, 1], -0.5957, 0.5957)
    q2 = np.clip(b * yiq[:, :, 2], -0.5226, 0.5226)

    r1g1b1 = np.zeros(yiq.shape)
    r1g1b1[:, :, 0] = np.clip(y1 + 0.9663 * i2 + 0.6210 * q2, 0, 1)
    r1g1b1[:, :, 1] = np.clip(y1 - 0.2721 * i2 - 0.6474 * q2, 0, 1)
    r1g1b1[:, :, 2] = np.clip(y1 - 1.1070 * i2 + 1.7046 * q2, 0, 1)

    ax5 = fig.add_subplot(gs[1:, 1:3])
    ax5.imshow(r1g1b1)
    ax5.set_title(f"Imagen Procesada (a={a}, b={b})")
    ax5.axis('off')

    plt.tight_layout()
    return fig

def importarImagen():
    global rutaImagen, canvasOriginal
    rutaImagen = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if rutaImagen:
        etiqueta["text"] = "Imagen importada correctamente!"
        mostrarImagen()
    else:
        etiqueta["text"] = "No se seleccionó ninguna imagen."

def mostrarImagen():
    global rutaImagen, canvasOriginal
    if rutaImagen:
        imagen = iio.imread(rutaImagen)
        imagen = np.clip(imagen / 255., 0., 1.)

        if canvasOriginal:
            canvasOriginal.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.imshow(imagen)
        ax.set_title("Imagen Original")
        ax.axis('off')

        canvasOriginal = FigureCanvasTkAgg(fig, master=tabImagenOriginal)
        canvasOriginal.get_tk_widget().pack(expand=True)
        canvasOriginal.draw()
    else:
        etiqueta["text"] = "Primero debes cargar una imagen!"

def procesarImagen():
    global rutaImagen, canvasProcesado
    if rutaImagen:
        imagen = iio.imread(rutaImagen)
        imagen = np.clip(imagen / 255., 0., 1.)

        procesamiento = tipoProcesamiento.get()
        if procesamiento == "Blanco y Negro":
            fig = procesarBlancoNegro(imagen)
        elif procesamiento == "Canal Rojo":
            fig = procesarCanal(imagen, 0, "Canal Rojo", 'Reds')
        elif procesamiento == "Canal Verde":
            fig = procesarCanal(imagen, 1, "Canal Verde", 'Greens')
        elif procesamiento == "Canal Azul":
            fig = procesarCanal(imagen, 2, "Canal Azul", 'Blues')
        elif procesamiento == "Luminancia y Saturacion":
            ventana.grab_set()
            a = simpledialog.askfloat("Luminancia", "Ingresa el valor para 'a':", parent=ventana)
            b = simpledialog.askfloat("Saturacion", "Ingresa el valor para 'b':", parent=ventana)
            ventana.grab_release()
            if a is not None and b is not None:
                fig = procesarLuminanciaSaturacion(imagen, a, b)
            else:
                etiqueta["text"] = "Operación cancelada."
                return
        elif procesamiento == "Canales RGB":
            fig = procesarCanalesRGB(imagen)

        if canvasProcesado:
            canvasProcesado.get_tk_widget().destroy()

        canvasProcesado = FigureCanvasTkAgg(fig, master=tabImagenProcesada)
        canvasProcesado.get_tk_widget().pack(expand=True)
        canvasProcesado.draw()
    else:
        etiqueta["text"] = "Primero debes cargar una imagen!"


#----------------------------------------------------------------#
# Configuración del interfaz de Tkinter
ventana = tk.Tk()
ventana.title("Trabajo Practico N°1 - Color")
ventana.geometry("1200x700")

# Crear un Notebook para organizar pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill='both')

# Crear las pestañas
tabImagenOriginal = ttk.Frame(notebook)
tabImagenProcesada = ttk.Frame(notebook)
tabControles = ttk.Frame(notebook)

notebook.add(tabImagenOriginal, text='Imagen Original')
notebook.add(tabImagenProcesada, text='Imagen Procesada')
notebook.add(tabControles, text='Controles')

# Configuración de controles
frameControles = tk.Frame(tabControles)
frameControles.pack(pady=10)

botonCargar = tk.Button(frameControles, text="Cargar Imagen", command=importarImagen)
botonCargar.grid(row=0, column=0, padx=10)

botonProcesar = tk.Button(frameControles, text="Procesar Imagen", command=procesarImagen)
botonProcesar.grid(row=0, column=2, padx=10)

etiqueta = tk.Label(frameControles, text="")
etiqueta.grid(row=1, columnspan=3, pady=3)

tipoProcesamiento = StringVar(value="Blanco y Negro")
opcionesProcesamiento = ["Blanco y Negro", "Canal Rojo", "Canal Verde", "Canal Azul", "Luminancia y Saturacion", "Canales RGB"]
menuProcesamiento = OptionMenu(frameControles, tipoProcesamiento, *opcionesProcesamiento)
menuProcesamiento.grid(row=0, column=1, padx=10)

ventana.mainloop()
