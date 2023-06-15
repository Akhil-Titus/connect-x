#0 left click
#1 right click
#2 double click
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import paho.mqtt.client as mqtt
import json
#import pyautogui as cursor

topicx = "topicx"
topicy = "topicy"
# Set up the MQTT client
mqtt_client = mqtt.Client()
localhost = "10.42.0.1"
# Connect to the broker 
mqtt_client.connect("localhost", 1883)

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://10.42.0.64:81/stream')

detector = HandDetector(maxHands=1)
classifier = Classifier("hand_model/best_model2.h5", "hand_model/labels.txt")

offset = 20

imgSize = 300

folder = "Data/C"
counter = 0

labels = ["un", "soldier", "intruder" ]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        if imgCrop.shape[0] == 0 or imgCrop.shape[1] == 0:
            continue
        anglex=int((x)/10)
        # angley=int(y)

        valueeX=str(anglex)
        # valueeY=str(angley)

        motorX =  valueeX
        # motorY = valueeY

        # mqtt_client.publish(topicx, motorX)

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)



        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                      (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset),
                      (x + w + offset, y + h + offset), (255, 0, 255), 4)

        #cv2.imshow("ImageCrop", imgCrop)
        #cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break
    cv2.waitKey(1)
