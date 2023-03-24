#Proyecto deteccion de objetivo por vision
#Mateo Burbano 2020

import cv2
import numpy as np
import RPi.GPIO as GPIO
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

GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)
GPIO.setup(out12,GPIO.OUT)
GPIO.setup(out22,GPIO.OUT)
GPIO.setup(out32,GPIO.OUT)
GPIO.setup(out42,GPIO.OUT)

print ("First calibrate by giving some +ve and -ve values.....")

#Iniciamos la camara
captura = cv2.VideoCapture(0)
 
while(1):
     
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _, imagen = captura.read()
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
 
    #Establecemos el rango de colores que vamos a detectar
    #En este caso de verde oscuro a verde-azulado claro
    verde_bajos = np.array([49,50,50], dtype=np.uint8)
    verde_altos = np.array([80, 255, 255], dtype=np.uint8)
 
    #Crear una mascara con solo los pixeles dentro del rango de verdes
    mask = cv2.inRange(hsv, verde_bajos, verde_altos)
 
    #Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mask)
    area = moments['m00']
 
    #Descomentar para ver el area por pantalla
    #print area
    if(area > 1000000):
         
        #Buscamos el centro x, y del objeto
        xcam = int(moments['m10']/moments['m00'])
        ycam = int(moments['m01']/moments['m00'])

        try:

          #GPIO.output(out1,GPIO.LOW)
          #GPIO.output(out2,GPIO.LOW)
          #GPIO.output(out3,GPIO.LOW)
          #GPIO.output(out4,GPIO.LOW)
          #GPIO.setup(out12,GPIO.LOW)
          #GPIO.setup(out22,GPIO.LOW)
          #GPIO.setup(out32,GPIO.LOW)
          #GPIO.setup(out42,GPIO.LOW)

          """if ycam>250 and cambio==0:
              for y2 in range(5,0,-1):
                  if negative2==1:
                      if i2==7:
                          i2=0
                      else:
                          i2=i2+1
                      y2=y2+2
                      negative2=0
                  positive2=1
                  #print((x+1)-y)
                  if i2==0:
                      GPIO.output(out12,GPIO.HIGH)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==1:
                      GPIO.output(out12,GPIO.HIGH)
                      GPIO.output(out22,GPIO.HIGH)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==2:  
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.HIGH)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==3:    
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.HIGH)
                      GPIO.output(out32,GPIO.HIGH)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==4:  
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.HIGH)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==5:
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.HIGH)
                      GPIO.output(out42,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==6:    
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==7:    
                      GPIO.output(out12,GPIO.HIGH)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  if i2==7:
                      i2=0
                      continue
                  i2=i2+1
          
          
          elif ycam<200 and cambio==0:
              for y2 in range(5,0,-1):
                  if positive2==1:
                      if i2==0:
                          i2=7
                      else:
                          i2=i2-1
                      y2=y2+3
                      positive2=0
                  negative2=1
                  #print((x+1)-y) 
                  if i2==0:
                      GPIO.output(out12,GPIO.HIGH)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==1:
                      GPIO.output(out12,GPIO.HIGH)
                      GPIO.output(out22,GPIO.HIGH)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==2:  
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.HIGH)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==3:    
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.HIGH)
                      GPIO.output(out32,GPIO.HIGH)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==4:  
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.HIGH)
                      GPIO.output(out42,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==5:
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.HIGH)
                      GPIO.output(out42,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==6:    
                      GPIO.output(out12,GPIO.LOW)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i2==7:    
                      GPIO.output(out12,GPIO.HIGH)
                      GPIO.output(out22,GPIO.LOW)
                      GPIO.output(out32,GPIO.LOW)
                      GPIO.output(out42,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  if i2==0:
                      i2=7
                      continue
                  i2=i2-1
                  
          elif ycam>200 and ycam<250 and cambio==0:
              #cambio = 1
              cambio = 0"""


          
          if xcam>350 and cambio==1:
              for y in range(1,0,-1):
                  if negative==1:
                      if i==7:
                          i=0
                      else:
                          i=i+1
                      y=y+2
                      negative=0
                  positive=1
                  #print((x+1)-y)
                  if i==0:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  if i==7:
                      i=0
                      continue
                  i=i+1
          
          
          elif xcam<300 and cambio==1:
              for y in range(1,0,-1):
                  if positive==1:
                      if i==0:
                          i=7
                      else:
                          i=i-1
                      y=y+3
                      positive=0
                  negative=1
                  #print((x+1)-y) 
                  if i==0:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.03)
                      #time.sleep(1)
                  if i==0:
                      i=7
                      continue
                  i=i-1

          elif xcam>300 and xcam<350 and cambio==1:
              cambio = 1

        except KeyboardInterrupt:
            GPIO.cleanup()
         
        #Mostramos sus coordenadas por pantalla
        print ("x = ", xcam)
        print ("y = ", ycam)
 
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (xcam-5, ycam-5), (xcam+5, ycam+5),(0,0,255), 2)
        cv2.putText(imagen, "pos:"+ str(xcam)+","+str(ycam), (xcam+10,ycam+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
     
    #Mostramos la imagen original con la marca del centro y
    #la mascara
    cv2.imshow('mask', mask)
    cv2.imshow('Camara', imagen)
    
    #tecla = cv2.waitKey(5) & 0xFF
    if cv2.waitKey(1) & 0xFF == ord('q'):
        captura.release()
        break
 
cv2.destroyAllWindows()
