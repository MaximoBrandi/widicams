import cv2
import face_recognition
import numpy as np
import dlib

# Inicializar algunos arrays
known_face_encodings = []
known_face_names = []

# Cargar una imagen y aprender a reconocerla.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Agregar la codificación de cara y el nombre a los arrays
known_face_encodings.append(obama_face_encoding)
known_face_names.append("Barack Obama")

# Inicializar algunas variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Inicializar la webcam
video_capture = cv2.VideoCapture(0)

# Inicializar el detector de caras de dlib (HOG-based)
detector = dlib.get_frontal_face_detector()

# Inicializar el predictor de puntos de referencia faciales de dlib
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    # Capturar un solo fotograma de video
    ret, frame = video_capture.read()

    # Redimensionar el fotograma de video a 1/4 de tamaño para procesamiento más rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convertir la imagen de BGR (utilizada por OpenCV) a RGB (utilizada por face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Solo procesar cada otro fotograma de video para ahorrar tiempo
    if process_this_frame:
        # Buscar todas las caras en el fotograma de video actual
        face_locations = detector(rgb_small_frame)

        # Codificar las caras encontradas en el fotograma de video actual
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Inicializar una lista de nombres de caras encontradas
        face_names = []

        # Para cada cara encontrada, buscar si es una cara conocida
        for face_encoding in face_encodings:
            # Buscar si la cara actual coincide con una cara conocida
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconocido"

            # Si hay una coincidencia, usar el nombre de la cara conocida como etiqueta
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Agregar el nombre de la cara encontrada a la lista de nombres de caras encontradas
            face_names.append(name)

    process_this_frame = not process_this_frame

    # Mostrar los resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Escalar las ubicaciones de las caras encontradas en el fotograma de video original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Dibujar un cuadro alrededor de la cara y agregar una etiqueta de nombre
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
           frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

# Mostrar el fotograma de video resultante
cv2.imshow('Video', frame)

# Si se presiona 'q', salir del bucle
if cv2.waitKey(1) & 0xFF == ord('q'):
    break