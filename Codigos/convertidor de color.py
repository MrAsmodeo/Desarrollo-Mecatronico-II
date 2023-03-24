import numpy as np
import cv2

# Convertir el color de formato RGB a formato HSV
color_rgb = np.uint8([[[134, 44, 132]]])  # aquí debes colocar los valores de tu color en formato RGB
color_hsv = cv2.cvtColor(color_rgb, cv2.COLOR_BGR2HSV)

# Establecer el rango para el color en formato HSV
lower_color = np.array([color_hsv[0][0][0]-10, color_hsv[0][0][1]-50, color_hsv[0][0][2]-50])
upper_color = np.array([color_hsv[0][0][0]+10, color_hsv[0][0][1]+50, color_hsv[0][0][2]+50])

# Imprimir el rango para verificar
print("Rango para el color: ", lower_color, "-", upper_color)
