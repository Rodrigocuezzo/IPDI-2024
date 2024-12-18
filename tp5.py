import cv2
import numpy as np

# 1. Binarización simple

def binarizacion_media(image):
    umbral = np.mean(image)
    _, binarizada = cv2.threshold(image, umbral, 255, cv2.THRESH_BINARY)
    return binarizada

def binarizacion_moda(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    moda = np.argmax(hist)
    _, binarizada = cv2.threshold(image, moda, 255, cv2.THRESH_BINARY)
    return binarizada

def binarizacion_otsu(image):
    _, binarizada = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binarizada

# 2. Detección de bordes

def bordes_laplaciano(image):
    laplaciano = cv2.Laplacian(image, cv2.CV_64F)
    return cv2.convertScaleAbs(laplaciano)

def bordes_morfologicos(image, kernel):
    dilatada = cv2.dilate(image, kernel)
    erosionada = cv2.erode(image, kernel)
    gradiente = cv2.subtract(dilatada, erosionada)
    return gradiente

def marching_squares(image):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# 3. Color fill con "varita mágica"

def color_fill(image, seed_point, new_value):
    filled = image.copy()
    mask = np.zeros((image.shape[0] + 2, image.shape[1] + 2), np.uint8)
    cv2.floodFill(filled, mask, seed_point, new_value)
    return filled

def main():
    # Las imágenes de prueba
    image_a_path = "C:\\Users\\Rodrigo\\Documents\\imagen1.jpg"  # ruta de la imagen a
    image_b_path = "C:\\Users\\Rodrigo\\Documents\\imagen2.jpg"  # ruta de la imagen b

    image_a = cv2.imread(image_a_path, cv2.IMREAD_GRAYSCALE)
    image_b = cv2.imread(image_b_path, cv2.IMREAD_GRAYSCALE)

    if image_a is None or image_b is None:
        print("Error: No se pudo cargar una o ambas imágenes")
        return

    # Binarización de la imagen (a)
    bin_media = binarizacion_media(image_a)
    bin_moda = binarizacion_moda(image_a)
    bin_otsu = binarizacion_otsu(image_a)

    # Detección de bordes en la imagen (a)
    kernel = np.ones((3, 3), np.uint8)
    bordes_lap = bordes_laplaciano(image_a)
    bordes_morfo = bordes_morfologicos(image_a, kernel)

    # Detectar bordes con marching squares
    contours = marching_squares(bin_otsu)
    image_a_contours = cv2.cvtColor(bin_otsu, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image_a_contours, contours, -1, (0, 255, 0), 1)

    # Implementar color fill en la imagen (b)
    seed_point = (50, 50)  # Cambiar por una posición inicial válida
    filled_image = color_fill(image_b, seed_point, 128)

    # Mostrar y guardar resultados
    cv2.imshow("Original A", image_a)
    cv2.imshow("Binarizacion Media", bin_media)
    cv2.imshow("Binarizacion Moda", bin_moda)
    cv2.imshow("Binarizacion Otsu", bin_otsu)
    cv2.imshow("Bordes Laplaciano", bordes_lap)
    cv2.imshow("Bordes Morfologicos", bordes_morfo)
    cv2.imshow("Marching Squares", image_a_contours)
    cv2.imshow("Color Fill B", filled_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
