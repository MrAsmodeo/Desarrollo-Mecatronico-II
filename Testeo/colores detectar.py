import cv2
import numpy as np

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Rango de colores a detectar (en formato HSV)
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
lower_blue = np.array([110, 100, 100])
upper_blue = np.array([130, 255, 255])

while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()

    # Convertir el frame a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obtener los píxeles que se encuentran dentro de los rangos de color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Aplicar un filtro morfológico para eliminar pequeños ruidos
    kernel = np.ones((5,5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

    # Encontrar los contornos de los objetos detectados
    contours_red, hierarchy = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, hierarchy = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, hierarchy = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos y mostrar el resultado
    cv2.drawContours(frame, contours_red, -1, (0, 0, 255), 2)
    cv2.drawContours(frame, contours_green, -1, (0, 255, 0), 2)
    cv2.drawContours(frame, contours_blue, -1, (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
