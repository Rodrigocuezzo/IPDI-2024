import cv2
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import os

# Función para cargar imágenes y etiquetas del dataset
def cargar_dataset(ruta_dataset):
    imagenes = []
    etiquetas = []
    for etiqueta in os.listdir(ruta_dataset):
        ruta_clase = os.path.join(ruta_dataset, etiqueta)
        if os.path.isdir(ruta_clase):
            for archivo in os.listdir(ruta_clase):
                ruta_imagen = os.path.join(ruta_clase, archivo)
                imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
                if imagen is not None:
                    imagen_redimensionada = cv2.resize(imagen, (100, 100))
                    imagenes.append(imagen_redimensionada)
                    etiquetas.append(etiqueta)
    return np.array(imagenes), np.array(etiquetas)

# Función para aplicar filtrado de preprocesamiento a las imágenes
def preprocesar_imagenes(imagenes):
    imagenes_procesadas = []
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])  # Filtro Laplaciano
    for imagen in imagenes:
        imagen_filtrada = cv2.filter2D(imagen, -1, kernel)
        imagen_normalizada = cv2.normalize(imagen_filtrada, None, 0, 255, cv2.NORM_MINMAX)
        imagenes_procesadas.append(imagen_normalizada)
    return np.array(imagenes_procesadas)

# Cargar dataset
ruta_dataset = "C:\\Users\\Rodrigo Nicolas\\Music\\FOTOSPROYECTO" # ruta de mi dataset 
imagenes, etiquetas = cargar_dataset(ruta_dataset)

# Preprocesar imágenes
imagenes_procesadas = preprocesar_imagenes(imagenes)

# Aplanar imágenes para entrenamiento
num_imagenes, alto, ancho = imagenes_procesadas.shape
imagenes_aplanadas = imagenes_procesadas.reshape(num_imagenes, alto * ancho)

# Escalar datos
scaler = StandardScaler()
imagenes_escaladas = scaler.fit_transform(imagenes_aplanadas)

# Codificar etiquetas
encoder = LabelEncoder()
etiquetas_codificadas = encoder.fit_transform(etiquetas)

# Dividir dataset en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(imagenes_escaladas, etiquetas_codificadas, test_size=0.2, random_state=42)

# Búsqueda de hiperparámetros para SVM
param_grid = {
    'C': [0.1, 1, 10],
    'gamma': ['scale', 'auto'],
    'kernel': ['rbf', 'linear']
}

modelo = GridSearchCV(SVC(probability=True), param_grid, cv=3, scoring='precision')
modelo.fit(X_train, y_train)

# Evaluamos el modelo
y_pred = modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy * 100:.2f}%")
print("Reporte de clasificación:\n", classification_report(y_test, y_pred, target_names=encoder.classes_))

# Reconocimiento facial en tiempo real
def reconocimiento_tiempo_real():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])  # Filtro Laplaciano

    cap = cv2.VideoCapture(0)
    print("Presiona 'e' para salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            rostro = gray[y:y+h, x:x+w]
            rostro_redimensionado = cv2.resize(rostro, (100, 100))
            rostro_filtrado = cv2.filter2D(rostro_redimensionado, -1, kernel)
            rostro_normalizado = cv2.normalize(rostro_filtrado, None, 0, 255, cv2.NORM_MINMAX)
            rostro_aplanado = scaler.transform(rostro_normalizado.flatten().reshape(1, -1))

            prediccion = modelo.predict(rostro_aplanado)
            etiqueta_predicha = encoder.inverse_transform(prediccion)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, etiqueta_predicha[0], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow('Reconocimiento Facial en Tiempo Real', frame)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

    cap.release()
    cv2.destroyAllWindows()

reconocimiento_tiempo_real()

