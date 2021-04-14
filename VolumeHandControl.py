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

# 输入的视频，“0”为打开摄像头
cap = cv2.VideoCapture("example2.mp4")
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
pLength = 0
detector = htm.handDetector()  # 创建对象

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()  # 静音
# volume.GetMasterVolumeLevel()  # 获取最大音量值
volRange = volume.GetVolumeRange()  # 获取音量范围
# print(volRange)
minVol = volRange[0]
maxVol = volRange[1]

# 显示栏音量与系统音量转换规则（两者不是线性的，这只是大概）
standard = {0: '100', -1: '94', -2: '88', -3: '82', -4: '77', -5: '72', -6: '67', -7: '63', -8: '59', -9: '55',
            -10: '51', -11: '48', -12: '45', -13: '42', -14: '39', -15: '36', -16: '34', -17: '32', -18: '30',
            -19: '30', -20: '26', -21: '24', -22: '22', -23: '21', -24: '20', -25: '18', -26: '17', -27: '16',
            -28: '15', -29: '14', -30: '13', -31: '12', -32: '11', -33: '10', -34: '9', -35: '9', -36: '8', -37: '8',
            -38: '7', -39: '6', -40: '6', -41: '5', -42: '5', -43: '5', -44: '4', -45: '4', -46: '4', -47: '3',
            -48: '3', -49: '3', -50: '2', -51: '2', -52: '2', -53: '2', -54: '2', -55: '1', -56: '1', -57: '1',
            -58: '1', -59: '1', -60: '1', -61: '0', -62: '0', -63: '0', -64: '0', -65: '0', -66: '0', -67: '0',
            -68: '0', -69: '0', -70: '0', -71: '0', -72: '0', -73: '0', -74: '0', -75: '0', -76: '0', -77: '0',
            -78: '0', -79: '0', -80: '0', -81: '0', -82: '0', -83: '0', -84: '0', -85: '0', -86: '0', -87: '0',
            -88: '0', -89: '0', -90: '0', -91: '0', -92: '0', -93: '0', -94: '0', -95: '0', -96: '0', -97: '0',
            -98: '0'}

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

        cLength = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        ranLength = abs(cLength - pLength)
        # print(ranLength)

        # Hand range 50-300（根据实际情况自己修改）
        vol = np.interp(cLength, [50, 300], [minVol, maxVol])  # interp()是进行线性内插，返回一个与length同形状的数
        volBar = np.interp(cLength, [50, 300], [400, 150])
        volPer = standard[int(vol)]

        # 改变距离大于10才会改变音量
        if ranLength >= 10:
            volume.SetMasterVolumeLevel(int(vol), None)  # 设置音量值

        if int(cLength) <= 50:
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # 绘制音量图
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)  # 外框
        if ranLength >= 10:
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, str(int(volPer)) + "%", (50, 430), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 2)
        else:
            fixVolume = volume.GetMasterVolumeLevel()
            fixLength = np.interp(fixVolume, [minVol, maxVol], [50, 300])
            fixVolBar = np.interp(fixLength, [50, 300], [400, 150])
            fixVolPer = standard[int(fixVolume)]
            # print(fixVolPer)
            cv2.rectangle(img, (50, int(fixVolBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, str(int(fixVolPer)) + "%", (50, 430), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 2)

        pLength = cLength

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS:" + str(int(fps)), (20, 30), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
