#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author:Dong Time:2021/4/12
import cv2
import mediapipe as mp
import time

# 获取视频对象，0为摄像头，也可以写入视频路径
cap = cv2.VideoCapture("example.mp4")

# 参考资料：https://google.github.io/mediapipe/solutions/hands.html
mpHands = mp.solutions.hands
# Hands是一个类，有四个初始化参数，static_image_mode,max_num_hands,min_detection_confidence,min_tracking_confidence
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils  # 画

pTime = 0  # 开始时间初始化
cTime = 0  # 目前时间初始化

while True:
    # sucess是布尔型，读取帧正确返回True;img是每一帧的图像（BGR存储格式）
    success, img = cap.read()
    # 将一幅图像从一个色彩空间转换为另一个,返回转换后的色彩空间图像
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 处理RGB图像并返回手的标志点和检测到的每个手对象
    results = hands.process(imgRGB)
    # results.multi_hand_landmarks返回None或手的标志点坐标
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # landmark有21个（具体查阅上面的参考网址），id是索引，lm是x,y坐标
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)  # lm的坐标是点在图像中的比例坐标
                # h-height,w-weight图像的宽度和高度
                h, w, c = img.shape
                # 将landmark的比例坐标转换为在图像像元上的坐标
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # 将手的标志点个性化显示
                cv2.circle(img, (cx, cy), int(w / 50), (255, 0, 255), cv2.FILLED)
            # 在图像上绘制手的标志点和他们的连接线
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # 将帧率显示在图像上
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 1)
    # 在Image窗口上显示新绘制的图像img
    cv2.imshow("Image", img)
    # 这个函数是在一个给定的时间内(单位ms)等待用户按键触发;如果用户按下键，则继续执行后面的代码，如果用户没有按下键,则接续等待
    cv2.waitKey(1)
