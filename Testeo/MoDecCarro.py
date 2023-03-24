import cv2

# Cargar el clasificador de Haar para carros
modelo = cv2.CascadeClassifier('haarcascade_car.xml')

# Iniciar la captura de video
cap = cv2.VideoCapture(0)

while True:
    # Leer la imagen
    ret, imagen = cap.read()

    # Convertir la imagen a escala de grises
    grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detección de objetos
    objetos_detectados = modelo.detectMultiScale(grises, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Dibuja los rectángulos alrededor de los objetos detectados
    for (x, y, w, h) in objetos_detectados:
        cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostrar la imagen resultante
    cv2.imshow('Detección de carros', imagen)

    # Salir si se presiona la tecla "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()

