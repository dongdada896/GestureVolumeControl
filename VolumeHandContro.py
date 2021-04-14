#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author:Dong Time:2021/4/13
import cv2
import time
import numpy as np
import HandTrackingMoudle as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########################
wCam, hCam = 640, 480
########################

cap = cv2.VideoCapture("example.mp4")
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector()  # 创建对象

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()  # 静音
# volume.GetMasterVolumeLevel()  # 获取最大音量值
volRange = volume.GetVolumeRange()  # 获取音量范围
minVol = volRange[0]
maxVol = volRange[1]

while True:

    sucess, img = cap.read()
    # 检测手
    img = detector.findHands(img)
    # 检测手的标志，并返回标志点坐标
    lmList = detector.findPosition(img, personDraw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        # 计算食指和大拇指指尖坐标，并绘制点、连线
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range 50-300（根据实际情况自己修改）
        vol = np.interp(length, [50, 300], [minVol, maxVol])  # interp()是进行线性内插，返回一个与length同形状的数
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        volume.SetMasterVolumeLevel(int(vol), None)  # 设置音量值

        if int(length) <= 50:
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # 绘制音量图
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, str(int(volPer)) + "%", (50, 430), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS:" + str(int(fps)), (20, 30), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
