import cv2
import numpy as np
import time 

out1 = 13
out2 = 11
out3 = 15
out4 = 12
out12 = 22
out22 = 18
out32 = 24
out42 = 16

i=0
positive=0
negative=0
y=0

i2=0
positive2=0
negative2=0
y2=0

cambio=1

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(out1,GPIO.OUT)
#GPIO.setup(out2,GPIO.OUT)
#GPIO.setup(out3,GPIO.OUT)
#GPIO.setup(out4,GPIO.OUT)
#GPIO.setup(out12,GPIO.OUT)
#GPIO.setup(out22,GPIO.OUT)
#GPIO.setup(out32,GPIO.OUT)
#GPIO.setup(out42,GPIO.OUT)

print ("First calibrate by giving some +ve and -ve values.....")

# Iniciamos la camara
captura = cv2.VideoCapture(0) # 0 es el número de dispositivo de la cámara principal

while(1):
     
    # Capturamos una imagen y la convertimos de RGB -> HSV
    _, imagen = captura.read()
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
 
    # Establecemos el rango de colores que vamos a detectar
    # En este caso de verde oscuro a verde-azulado claro
    verde_bajos = np.array([49,50,50], dtype=np.uint8)
    verde_altos = np.array([80, 255, 255], dtype=np.uint8)
 
    # Crear una mascara con solo los pixeles dentro del rango de verdes
    mask = cv2.inRange(hsv, verde_bajos, verde_altos)
 
    # Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mask)
    area = moments['m00']
 
    # Descomentar para ver el area por pantalla
    # print area
    if(area > 1000000):
         
        # Buscamos el centro x, y del objeto
        xcam = int(moments['m10']/moments['m00'])
        ycam = int(moments['m01']/moments['m00'])

        #try:

          # GPIO.output(out1,GPIO.LOW)
          # GPIO.output(out2,GPIO.LOW)
          # GPIO.output(out3,GPIO.LOW)
          # GPIO.output(out4,GPIO.LOW)
          # GPIO.setup(out12,GPIO.LOW)
          # GPIO.setup(out22,GPIO.LOW)
         
