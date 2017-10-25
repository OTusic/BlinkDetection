import numpy as np
import cv2
import time
from serial import Serial, SerialException

# for mac
cxn = Serial('/dev/tty.usbmodem1411', baudrate=9600)

# for ubuntu?

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#videoCapture.set(CV_CAP_PROP_FRAME_WIDTH, 500)
#videoCapture.set(CV_CAP_PROP_FRAME_HEIGHT, 600)
cap = cv2.VideoCapture(0)
last_reads = [0,0,0,0,0,0,0,0,0,0]
while 1:
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		if h%2 == 0:
			roi_color = img[y:int(y+(h/2)), x:x+w]
		else:
			roi_color = img[y:int(y+(h/2+0.5)), x:x+w]
		
		eyes = eye_cascade.detectMultiScale(roi_gray)
		actual_eyes = 0
		for (ex,ey,ew,eh) in eyes:
			#print(ey, eh, y, h)
			print(y,h)
			if eh<=0.4*h:
				actual_eyes += 1
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		if actual_eyes==1:
			last_reads.append(1)
		else:
			last_reads.append(0)
		last_reads.pop(0)
		if sum(last_reads) >= 5:
			print('Blink')
			cxn.write([1])

	cv2.imshow('img',img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
