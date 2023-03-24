import cv2
import numpy as np

# Función para detectar el color
def detect_color(frame):
    # Convertir el marco a formato HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definir los rangos de los colores a detectar
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([70, 255, 255])
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    
    # Definir una máscara para cada color
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    
    # Obtener el área de cada máscara
    red_area = cv2.countNonZero(red_mask)
    green_area = cv2.countNonZero(green_mask)
    blue_area = cv2.countNonZero(blue_mask)
    yellow_area = cv2.countNonZero(yellow_mask)
    
    # Determinar el color con el área más grande
    color = ''
    max_area = max(red_area, green_area, blue_area, yellow_area)
    if max_area == red_area:
        color = 'Rojo'
    elif max_area == green_area:
        color = 'Verde'
    elif max_area == blue_area:
        color = 'Azul'
    elif max_area == yellow_area:
        color = 'Amarillo'
    
    return color

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    # Leer un marco de la cámara
    ret, frame = cap.read()
    
    # Detectar el color
    color = detect_color(frame)
    
    # Mostrar el nombre del color en el marco
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, color, (50, 50), font, 1, (255, 255, 255), 2)
    
    # Mostrar el marco en una ventana
    cv2.imshow('Frame', frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
