import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Captura de video desde la cámara

lower_blue = np.array([0, 50, 50])  #Rango para detectar el Color Azul, provicional 
upper_blue = np.array([10, 255, 255])

# Posición anterior para Azul 
prev_pos = None

while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()

    # Convertir el frame a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obtener los píxeles que se encuentran dentro del rango de azul
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Aplicar un filtro morfológico para eliminar pequeños ruidos
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Encontrar los contornos de los objetos detectados
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Seleccionar el objeto azul más grande
    max_area = 0
    selected_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            selected_contour = contour

    # Si se ha detectado un objeto azul, dibujar el contorno y mostrar su posición
    if selected_contour is not None:
        cv2.drawContours(frame, [selected_contour], 0, (0,255,0), 2)
        M = cv2.moments(selected_contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.putText(frame, f'Partner ({cx}, {cy})', (cx, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Mostrar la posición del objeto si ha cambiado desde el frame anterior
        current_pos = (cx, cy)
        if prev_pos is None or current_pos != prev_pos:
            print("Posición del objeto azul: ({}, {})".format(current_pos[0], current_pos[1]))
            prev_pos = current_pos

    # Mostrar el resultado
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
