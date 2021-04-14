#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author:Dong Time:2021/4/12
import cv2
import time
import HandTrackingMoudle as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture('example.mp4')
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    cv2.waitKey(1)
