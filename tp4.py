import cv2
import numpy as np

#FUNCIONES MORFOLOGICAS 
def erosion(image, kernel):
    return cv2.erode(image, kernel, iterations=1)

def dilatacion(image, kernel):
    return cv2.dilate(image, kernel, iterations=1)

def apertura(image, kernel):
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def cierre(image, kernel):
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def borde_exterior(image, kernel):
    dilated = dilatacion(image, kernel)
    return cv2.subtract(dilated, image)

def borde_interior(image, kernel):
    eroded = erosion(image, kernel)
    return cv2.subtract(image, eroded)

def gradiente(image, kernel):
    dilated = dilatacion(image, kernel)
    eroded = erosion(image, kernel)
    return cv2.subtract(dilated, eroded)

def mediana(image):
    return cv2.medianBlur(image, 3)

def aplicar_filtro_secuencial(image, filtros):
    procesada = image.copy()
    for filtro in filtros:
        procesada = filtro(procesada)
    return procesada

def main():
    # Cargar la imagen en niveles de gris
    image_path = "C:\\Users\\Rodrigo\\Documents\\imagen en nivel de gris.jpg" # ruta de la imagen
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return

    # Crear elemento estructurante 3x3
    kernel = np.ones((3, 3), np.uint8)

    # Aplicar operaciones morfológicas
    eroded = erosion(image, kernel)
    dilated = dilatacion(image, kernel)
    opened = apertura(image, kernel)
    closed = cierre(image, kernel)
    exterior = borde_exterior(image, kernel)
    interior = borde_interior(image, kernel)
    gradient = gradiente(image, kernel)
    median_filtered = mediana(image)

    # Guardar y mostrar resultados
    cv2.imshow("Original", image)
    cv2.imshow("Erosion", eroded)
    cv2.imshow("Dilatacion", dilated)
    cv2.imshow("Apertura", opened)
    cv2.imshow("Cierre", closed)
    cv2.imshow("Borde Exterior", exterior)
    cv2.imshow("Borde Interior", interior)
    cv2.imshow("Gradiente", gradient)
    cv2.imshow("Mediana", median_filtered)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
