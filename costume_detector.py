import cv2
import mediapipe as mp
import numpy as np
import math
import time

from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import paho.mqtt.client as mqtt
import json

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://10.42.0.64:81/stream')

detector = HandDetector(maxHands=1)
classifier = Classifier("Model/costume_model.h5", "Model/labels.txt")


offset = 10
imgSize = 300

labels = ["soldier", "Soldier" ]

# Create a BodyPose object
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    success, img = cap.read()

    # Flip the image horizontally
    img = cv2.flip(img, 1)

    # Convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect poses in the image
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # Get the landmarks of the detected body
        landmarks = results.pose_landmarks.landmark

        # Calculate the bounding box coordinates
        x_min = min(landmark.x for landmark in landmarks)
        y_min = min(landmark.y for landmark in landmarks)
        x_max = max(landmark.x for landmark in landmarks)
        y_max = max(landmark.y for landmark in landmarks)

        # Scale the coordinates based on the image dimensions
        x = int(x_min * img.shape[1])
        y = int(y_min * img.shape[0])
        w = int((x_max - x_min) * img.shape[1])
        h = int((y_max - y_min) * img.shape[0])

        # Draw the bounding box on the image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape
         # Check if imgCrop dimensions are valid
        if imgCrop.shape[0] == 0 or imgCrop.shape[1] == 0:
            continue

        aspectRatio = h / w
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

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
            print(prediction, index)

      #  cv2.rectangle(img, (x - offset, y - offset - 50),
       #               (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 0), 2)
        #cv2.rectangle(img, (x - offset, y - offset),
         #             (x + w + offset, y + h + offset), (255, 0, 255), 4)

        #cv2.imshow("ImageCrop", imgCrop)
    # cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        # Save the image or perform any desired action
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print("Image saved!")

    if key == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
