# -*- coding: utf-8 -*-
"""
Created on Sat May 13 20:30:09 2023

@author: danie
"""

#Ocupados dias pero Bueno damo inico 

"""En este punto primero seria usar las librerias necesarias
la idea esta en comenzar paso a paso para que el codigo se 
de la mejor manera eh entendible para que todos lo puedan hacer
espero se cumplan las especta"""


#######Antes que nada organizar la estructura para realizar el codigo #########


#Primero seria realizar un codigo que nos permita poder determinar los colores
#despues de todo si lo realizamos a blancos y negros no es lo mismo

### Algoritmia para realizar el priyecto 

"""
1* Configuracion Inicial 
        - Primero nos Aeguramos de tener todas las herramientas
        necesarias instaladas como lo son Python, OpenCv, Bibliotes de deteccion de objetivos
        Control Bluethoo
        -Conectar el Modulo Bluetooh al ESP32 y asegurarnos de que este funcionando correctamente
        
2* Detección de Colores 
        - Utilizaremos para esto Opencv para detectar los colores de interes: Azul para el carro
        Amarillo para la pelota y Violeta o Rojo para el enemigo
        - Podriamos utilizar tecnicas como la segmoentacion de color para detectar los objetivos de 
        de interes en cada fotograma capturado por la camara

3* Orientacion del carro:
        - Podriamos plantar la dettecion de colores para localizar la pelota y determinar su centro.
        -Calcular la posicion relativa del centro de la pelota en relacion con el centro del cuadrado de
        vision de la camara
        - Si el centro de la pelota esta desplasado hacia un lado, el carro debera girar en la direccion adecuda para manterla en el centro

4* Contorl de movimiento 
        - Para eloo utilizamos el modulo Bluetoooth y el ESP32 para recibir los comando de control desde el Pc o raspberry 
        - Pese a que es un carro con llantas obnidireccionales usaremos solo 5 comandos de los 10
        - Configurar y comporbas que se envian las instrucciones de movimiento al ESP32 a traves del modulo para que el carro 
        ejecute las acciones correspondientes

5* Navegacion y evasion de obstaculos:
        -Implementa algoritmos de navegación para que el carro se acerque a la pelota y la lleve hasta el punto de referencia que 
        representa la cancha.
        - Si se detecta la presencia de un objeto de color violeta o rojo (enemigo) en el camino hacia la pelota, utiliza algoritmos
        de evasión de obstáculos para evitarlo.
        - Se puede utilizar técnicas como el seguimiento visual de la pelota y la planificación de trayectorias para lograr una navegación
        eficiente
    
6* Detención en la cancha
        -Una vez que el carro llegue al punto de referencia que representa la cancha, envía la instrucción de detenerse a través del módulo
        Bluetooth.
        -Asegúrarse de que el carro se detenga por completo y que mantenga su posición en la cancha.

7* Pruebas y ajustes
        -Realizar pruebas iterativas para verificar el funcionamiento del sistema y hacer ajustes necesarios en el código.
        -Asegúrase de que el carro pueda seguir y acercarse correctamente a la pelota, evadir obstáculos y detenerse en la cancha.
"""

### Primero seria realiar el codigo para la deteccion de colores 


"""

import cv2
import numpy as np

# Define el rango de colores que deseas detectar en formato HSV
lower_blue = np.array([80, 50, 50])
upper_blue = np.array([300, 255, 255])
lower_yellow = np.array([40, 40, 50])
upper_yellow = np.array([90, 255, 255])
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

# Inicia la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Captura un frame de la cámara web
    ret, frame = cap.read()

    # Convierte el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detecta los colores en el rango especificado
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    red_mask1 = cv2.inRange(hsv, lower_red, upper_red)
    red_mask2 = cv2.inRange(hsv, np.array([170, 50, 50]), np.array([180, 255, 255]))
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Aplica una máscara para obtener solo los píxeles que pertenecen a los colores detectados
    blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)
    yellow_res = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    red_res = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Muestra los resultados en la pantalla
    cv2.imshow('Blue', blue_res)
    cv2.imshow('Yellow', yellow_res)
    cv2.imshow('Red', red_res)

    # Espera a que el usuario presione la tecla 'q' para salir del programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara web y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()

"""

## Continuamos con el codigo General el cual nos permita obtener distancia y angulos 
"""
import cv2
import numpy as np

blue_center = None

def detect_colors(frame):
    # Convertir el fotograma de BGR a HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir los rangos de los colores a detectar
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([150, 255, 255])
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Filtrar los colores en el rango especificado
    mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask_red = mask_red + mask_red2

    return mask_blue, mask_yellow, mask_red


def process_contours(frame_with_contour, contours, color, label):
    global blue_center

    max_contour = max(contours, key=cv2.contourArea) if contours else None

    if max_contour is not None:
        cv2.drawContours(frame_with_contour, [max_contour], -1, color, 2)

        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(frame_with_contour, (cx, cy), 5, (255, 255, 255), -1)

            peri = cv2.arcLength(max_contour, True)
            approx = cv2.approxPolyDP(max_contour, 0.04 * peri, True)

            triangle_center = np.mean(approx, axis=0, dtype=int)[0]

            max_distance = 0
            main_vertex_index = 0

            for i, vertex in enumerate(approx):
                distance = np.linalg.norm(triangle_center - vertex[0])
                if distance > max_distance:
                    max_distance = distance
                    main_vertex_index = i

            main_vertex = approx[main_vertex_index][0]
            if label == 'Blue':
                cv2.line(frame_with_contour, tuple(triangle_center), tuple(main_vertex), (255, 0, 0), 2)
                angle = np.degrees(np.arctan2(main_vertex[1] - triangle_center[1], main_vertex[0] - triangle_center[0]))
                cv2.putText(frame_with_contour, f"Angulo: {angle:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0), 2)
                
                blue_center = triangle_center
        
            elif label == 'Yellow':
                cv2.circle(frame_with_contour, tuple(triangle_center), 5, (0, 255, 255), -1)
                yellow_center = triangle_center
                distance_blue_yellow = np.linalg.norm(blue_center - yellow_center)
                distance_yellow_reference = np.linalg.norm(yellow_center - (500, 250))
                cv2.putText(frame_with_contour, f"Distancia Azul-Amarillo: {distance_blue_yellow:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame_with_contour, f"Distancia Amarillo-Referencia: {distance_yellow_reference:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame_with_contour, " ", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                  


def Cancha(frame_with_contour, width, height):
# Dibujar rectángulo en todo el campo
    cv2.rectangle(frame_with_contour, (0, 0), (width, height), (255, 0, 0), 2)
    # Dibujar punto de referencia para tu cancha
    cv2.circle(frame_with_contour, (0,250), 5, (0, 255, 0), -1)
    cv2.putText(frame_with_contour, "Tu Cancha", (0,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Dibujar punto de referencia para la cancha enemiga
    cv2.circle(frame_with_contour, (500,250), 5, (0, 0, 255), -1)
    cv2.putText(frame_with_contour, "Cancha Enemiga", (500,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def calculate_distances(blue_center, yellow_center):
    distance_blue_yellow = np.linalg.norm(blue_center - yellow_center)
    distance_yellow_reference = np.linalg.norm(yellow_center - (500, 250))
    return distance_blue_yellow, distance_yellow_reference

def detect_and_display_colors():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
    
        if not ret:
            break
    
        mask_blue, mask_yellow, mask_red = detect_colors(frame)

        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame_with_contour = frame.copy()

        process_contours(frame_with_contour, contours_blue, (255, 0, 0), 'Blue')
        process_contours(frame_with_contour, contours_yellow, (0, 255, 255), 'Yellow')
        process_contours(frame_with_contour, contours_red, (148, 0, 211), 'Red')
    
        # Dibujamos el campo y los puntos de referencia
        Cancha(frame_with_contour, frame_with_contour.shape[1], frame_with_contour.shape[0])
        cv2.imshow("Field Detection", frame_with_contour)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
detect_and_display_colors()

 """
 
 
 #Despues de fallo y error 
import cv2
import numpy as np
# import serial
# import time


blue_center = None
yellow_center = None
robot_state = "SEARCHING"
min_distance_threshold = 50
#configuramos el puesto serie 

#port= 'COM5'
#baudrate = 9600

# Creamos objetivo comunicacion serial 

# #ser = serial.Serial(port, baudrate)
# time.sleep(2) # esperamos 2 segundos para la comunicacion 

# def enviar_comando(comando):
#     ser.write(comando.encode())
#     print(f"Comando enviado: {comando}")

# def detener_robot():
#     enviar_comando(" ")

# def mover_adelante():
#     enviar_comando("W")

# def mover_atras():
#     enviar_comando("S")

# def girar_izquierda():
#     enviar_comando("Q")

# def girar_derecha():
#     enviar_comando("E")


def detect_colors(frame):
    # Convertir el fotograma de BGR a HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir los rangos de los colores a detectar
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([150, 255, 255])
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Filtrar los colores en el rango especificado
    mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask_red = mask_red + mask_red2

    return mask_blue, mask_yellow, mask_red


def process_contours(frame_with_contour, contours, color, label):
    
    global blue_center
    global yellow_center
    global main_vertex
    global distance_blue_yellow
    global angle

  

    max_contour = max(contours, key=cv2.contourArea) if contours else None

    if max_contour is not None:
        cv2.drawContours(frame_with_contour, [max_contour], -1, color, 2)

        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(frame_with_contour, (cx, cy), 5, (255, 255, 255), -1)

            peri = cv2.arcLength(max_contour, True)
            approx = cv2.approxPolyDP(max_contour, 0.04 * peri, True)

            triangle_center = np.mean(approx, axis=0, dtype=int)[0]

            max_distance = 0
            main_vertex_index = 0

            for i, vertex in enumerate(approx):
                distance = np.linalg.norm(triangle_center - vertex[0])
                if distance > max_distance:
                    max_distance = distance
                    main_vertex_index = i

            main_vertex = approx[main_vertex_index][0]
            
            if label == 'Blue':
                cv2.line(frame_with_contour, tuple(triangle_center), tuple(main_vertex), (255, 0, 0), 2)
                angle = np.degrees(np.arctan2(triangle_center[1] - main_vertex[1], triangle_center[0] - main_vertex[0]))
                anglef = angle
                cv2.putText(frame_with_contour, f"Angulo: {anglef:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0), 2)
                
                blue_center = triangle_center
        
            elif label == 'Yellow':
                #cv2.circle(frame_with_contour, tuple(triangle_center), 5, (0, 255, 255), -1)
                yellow_center = triangle_center
                distance_blue_yellow = np.linalg.norm(blue_center - yellow_center)
                distance_yellow_reference = np.linalg.norm(yellow_center - (500, 250))
                cv2.putText(frame_with_contour, f"Distancia Azul-Amarillo: {distance_blue_yellow:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame_with_contour, f"Distancia Amarillo-Referencia: {distance_yellow_reference:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
                if blue_center is not None and yellow_center is not None:
                    
                    distance_blue_yellow = calculate_distances(blue_center, yellow_center)
                    cv2.putText(frame_with_contour, f"Distancia Azul-Amarillo: {distance_blue_yellow:.2f}", (10, 90),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame_with_contour, f"Distancia Amarillo-Referencia: {distance_yellow_reference:.2f}",(10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
                if blue_center is not None and yellow_center is not None:
                    cv2.line(frame_with_contour, tuple(blue_center), tuple(yellow_center), (0, 255, 0), 2)
                if blue_center is not None and (500,250):
                    cv2.line(frame_with_contour, tuple(blue_center), (500,250),(0,255,0),2)
                     
                if blue_center is not None and yellow_center is not None:
                    cv2.line(frame_with_contour, tuple(blue_center), tuple(yellow_center), (0, 255, 0), 2)

                    if label == 'Blue':
                        cv2.line(frame_with_contour, tuple(main_vertex), tuple(yellow_center), (0, 0, 255), 2)

            else:
                cv2.putText(frame_with_contour, " ", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


def Cancha(frame_with_contour, width, height):
# Dibujar rectángulo en todo el campo
    cv2.rectangle(frame_with_contour, (0, 0), (width, height), (255, 0, 0), 2)
    # Dibujar punto de referencia para tu cancha
    cv2.circle(frame_with_contour, (0,250), 5, (0, 255, 0), -1)
    cv2.putText(frame_with_contour, "Tu Cancha", (0,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Dibujar punto de referencia para la cancha enemiga
    cv2.circle(frame_with_contour, (500,250), 5, (0, 0, 255), -1)
    cv2.putText(frame_with_contour, "Cancha Enemiga", (500,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    
def calculate_distances(center_blue, center_yellow):
    distance_blue_yellow = np.linalg.norm(center_blue - center_yellow)
    return distance_blue_yellow

def calculate_angle(center_blue, center_yellow):
    
    dx = center_blue[0] - main_vertex[1]
    dy = center_blue[1] - main_vertex[0]
    angle= np.degrees(np.arctan2(dy, dx))
    return angle

# def controlar_robot(blue_center, yellow_center, robot_state, min_distance_threshold):
#     if robot_state == "SEARCHING":
#         if blue_center is not None and yellow_center is not None:
#             angle = calculate_angle(blue_center, yellow_center)
#             distance = calculate_distances(blue_center, yellow_center)
#             print(f"Ángulo: {angle:.2f}")
#             print(f"Distancia: {distance:.2f}")

#             if angle != 90:
#                 if distance > min_distance_threshold:
#                     if angle > 100:
#                         detener_robot()
#                     else:
#                         detener_robot()
#                 else:
#                     detener_robot()
#                     mover_adelante()
#                     robot_state = "CARRYING"
#             else:
#                 girar_derecha()
#     elif robot_state == "CARRYING":
#         if blue_center is not None and yellow_center is not None:
#             angle = calculate_angle(blue_center, yellow_center)
#             distance = calculate_distances(blue_center, yellow_center)
#             print(f"Ángulo: {angle:.2f}")
#             print(f"Distancia: {distance:.2f}")

#             if angle > 5 or angle < -5:
#                 if angle > 0:
#                     girar_derecha()
#                 else:
#                     girar_izquierda()
#             else:
#                 detener_robot()
#                 mover_adelante()
#     else:
#         detener_robot()  # Detiene el robot cerca de la pelota
#         robot_state = "FINISHED"  # Cambia el estado del robot a "FINISHED"

def controlar_robot(blue_center, yellow_center, robot_state, min_distance_threshold):
    
    if robot_state == "SEARCHING" or robot_state == "CARRYING":
        if blue_center is not None and yellow_center is not None:
            
            distance = distance_blue_yellow
            anglex = angle
            print(f"Ángulo: {anglex:.2f}")
            print(f"Distancia: {distance:.2f}")
            #print(f"Angulo test : {anglex:.2f}")
            
            stop_count = 0 
            if abs(angle) > 150:
                print('girar_Izquierda')
            
            if 146 <= abs(angle) <= 149:
                if stop_count < 4:  
                    stop_count += 1
                    print('Parar Giro')
                if stop_count == 20:
                    print("Parar ")
                if 130<= distance < 158:
                    print('Stop_avance')
                elif distance >= 160:
                    print('Avanza hasta el objetivo')
            if abs(angle) <= 145:
                    print ('girar_Derecha')

def detect_and_display_colors():
    cap = cv2.VideoCapture(0)
    
    global robot_state
    global blue_center
    global yellow_center
    
    while True:
        ret, frame = cap.read()
    
        if not ret:
            break
    
        mask_blue, mask_yellow, mask_red = detect_colors(frame)

        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame_with_contour = frame.copy()

        process_contours(frame_with_contour, contours_blue, (255, 0, 0), 'Blue')
        process_contours(frame_with_contour, contours_yellow, (0, 255, 255), 'Yellow')
        process_contours(frame_with_contour, contours_red, (148, 0, 211), 'Red')
    
        # Dibujamos el campo y los puntos de referencia
        Cancha(frame_with_contour, frame_with_contour.shape[1], frame_with_contour.shape[0])
        
        
        if robot_state == "SEARCHING" or robot_state == "CARRYING":
            controlar_robot(blue_center, yellow_center, robot_state, min_distance_threshold)

    
        cv2.imshow("Field Detection", frame_with_contour)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
detect_and_display_colors()