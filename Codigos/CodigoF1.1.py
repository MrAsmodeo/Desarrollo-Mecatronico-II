import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Captura de video desde la cámara

lower_blue = np.array([110, 50, 50])  #Rango para detectar el Color Azul, provicional 
upper_blue = np.array([130, 255, 255])
# ahora si biene lo chido para el Enemigo 
lower_violet = np.array([130, 50, 50])  #Rango para detectar el Color Azul, provicional 
upper_violet = np.array([300, 255, 255])
# para la pelota 
lower_yellow = np.array([20, 100, 100])  #Rango para detectar el Color Azul, provicional 
upper_yellow = np.array([40, 255, 255])
# Posición anterior para Azul 
prev_pos_blue = None
prev_pos_violet = None
prev_pos_yellow = None

while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()

    # Convertir el frame a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obtener los píxeles que se encuentran dentro del rango de azul
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    violet_mask = cv2.inRange(hsv,lower_violet, upper_violet)
    yellow_mask = cv2.inRange(hsv,lower_yellow, upper_yellow)


    # Aplicar un filtro morfológico para eliminar pequeños ruidos
    kernel = np.ones((5,5), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    violet_mask = cv2.morphologyEx(violet_mask,cv2.MORPH_OPEN,kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask,cv2.MORPH_OPEN,kernel)

    # Encontrar los contornos de los objetos detectados
    contours_blue, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_violet, hierarchy = cv2.findContours(violet_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Seleccionar el objeto azul más grande
    max_area_blue= 0
    selected_contour_blue = None
    for contour_blue in contours_blue:
        area_blue= cv2.contourArea(contour_blue)
        if area_blue > max_area_blue:
            max_area_blue = area_blue
            selected_contour_blue = contour_blue

    # Seleccionar el objeto Violet más grande
    max_area_violet= 0
    selected_contour_violet = None
    for contour_violet in contours_violet:
        area_violet= cv2.contourArea(contour_violet)
        if area_violet > max_area_violet:
            max_area_violet = area_violet
            selected_contour_violet = contour_violet

    # Seleccionar el objeto Yellow más grande
    max_area_yellow= 0
    selected_contour_yellow = None
    for contour_yellow in contours_yellow:
        area_yellow= cv2.contourArea(contour_yellow)
        if area_yellow > max_area_yellow:
            max_area_yellow = area_yellow
            selected_contour_yellow = contour_yellow

    # Si se ha detectado un objeto azul, dibujar el contorno y mostrar su posición
    if selected_contour_blue is not None:
        cv2.drawContours(frame, [selected_contour_blue], 0, (0,255,0), 2)
        M = cv2.moments(selected_contour_blue)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.putText(frame, f'Partner ({cx}, {cy})', (cx, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Mostrar la posición del objeto si ha cambiado desde el frame anterior
        current_pos_blue = (cx, cy)
        if prev_pos_blue is None or current_pos_blue != prev_pos_blue:
            print("Posición del objeto azul: ({}, {})".format(current_pos_blue[0], current_pos_blue[1]))
            prev_pos_blue = current_pos_blue
            
    # Si se ha detectado un objeto violet, dibujar el contorno y mostrar su posición
    if selected_contour_violet is not None:
        cv2.drawContours(frame, [selected_contour_violet], 0, (0,255,0), 2)
        M = cv2.moments(selected_contour_violet)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.putText(frame, f'Enemy ({cx}, {cy})', (cx, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Mostrar la posición del objeto si ha cambiado desde el frame anterior
        current_pos_violet = (cx, cy)
        if prev_pos_violet is None or current_pos_violet != prev_pos_violet:
            print("Posición del objeto Violeta: ({}, {})".format(current_pos_violet[0], current_pos_violet[1]))
            prev_pos_violet = current_pos_violet


    # Si se ha detectado un objeto yellow, dibujar el contorno y mostrar su posición
    if selected_contour_yellow is not None:
        cv2.drawContours(frame, [selected_contour_yellow], 0, (0,255,0), 2)
        M = cv2.moments(selected_contour_yellow)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.putText(frame, f'Pelota ({cx}, {cy})', (cx, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Mostrar la posición del objeto si ha cambiado desde el frame anterior
        current_pos_yellow = (cx, cy)
        if prev_pos_yellow is None or current_pos_yellow != prev_pos_violet:
            print("Posición del objeto Amarillo: ({}, {})".format(current_pos_yellow[0], current_pos_yellow[1]))
            prev_pos_yellow = current_pos_yellow


    # Mostrar el resultado
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()