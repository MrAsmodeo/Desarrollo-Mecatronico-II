import time
import numpy as np
import cv2
# Create our body classifier
car_classifier = cv2.CascadeClassifier('haarcascade_fullbody.xml')
# Initiate video capture for video file
cap = cv2.VideoCapture('express-train-139537.mp4')
# Loop once video is successfully loaded
while cap.isOpened():
    
    time.sleep(.05)
    # Read first frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    # Pass frame to our car classifier
    cars = car_classifier.detectMultiScale(gray, 1.1, 2)
    
    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in cars:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.imshow('Cars', frame)
   # Esperar a que se presione la tecla "q" para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()