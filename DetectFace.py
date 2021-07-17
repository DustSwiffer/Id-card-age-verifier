import Settings
import cv2
import numpy as np
import math

settings = Settings.Settings()


def findFacesOnIdCard(path):
    img = cv2.imread(path)
    face_cascade = cv2.CascadeClassifier('config/face_detector.xml')
    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return faces


def findFaceInVideoFrame(path):
    img = cv2.imread(path)
    face_cascade = cv2.CascadeClassifier('config/face_detector.xml')
    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return faces[0]


def Find(videoFramePath, idCardPath):
    face_cascade = cv2.CascadeClassifier('config/face_detector.xml')

    videoFrame = cv2.imread(videoFramePath)
    idCard = cv2.imread(idCardPath)

    grayVideoFrame = IncreaseBrightnessOfSelfie(videoFrame)

    facesInVideoFrame = face_cascade.detectMultiScale(grayVideoFrame, 1.2, 4)

    grayIdCard = cv2.cvtColor(idCard, cv2.COLOR_BGR2GRAY)
    facesInIdCard = face_cascade.detectMultiScale(grayIdCard, 1.2, 3)

    for (videoFrameX, videoFrameY, videoFrameW, videoFrameH) in facesInVideoFrame:
        roiGrayVideoFrame = grayVideoFrame[videoFrameY:videoFrameY + videoFrameH, videoFrameX:videoFrameX + videoFrameW]

        roiVideoFrameH = roiGrayVideoFrame.shape[0]
        roiVideoFrameW = roiGrayVideoFrame.shape[1]

        resizedVideoFrameRoI = cv2.resize(roiGrayVideoFrame, (int(roiVideoFrameH / 5), int(roiVideoFrameW / 5)))

        count = 0

        for (x, y, w, h) in facesInIdCard:
            count += 1
            roiGrayIdCard = grayIdCard[y:y + h, x:x + w]

            score = cv2.matchTemplate(roiGrayIdCard, resizedVideoFrameRoI, cv2.TM_CCOEFF_NORMED).max()
            confidenceInPercent = round(score * 100, 2)
            print("Confidence of face recognition in percent: " + str(confidenceInPercent))

            return score


def IncreaseBrightnessOfSelfie(videoFramePath):

    hsv = cv2.cvtColor(videoFramePath, cv2.COLOR_BGR2HSV)

    hue, sat, val = cv2.split(hsv)

    mid = float(settings.TesseractPath)
    mean = np.mean(val)
    gamma = math.log(mid * 255) / math.log(mean)

    valGamma = np.power(val, gamma).clip(0, 255).astype(np.uint8)

    hsv_gamma = cv2.merge([hue, sat, valGamma])

    gammaRGB = cv2.cvtColor(hsv_gamma, cv2.COLOR_HSV2BGR)
    grayVideoFrame = cv2.cvtColor(gammaRGB, cv2.COLOR_BGR2GRAY)

    return np.power(grayVideoFrame, gamma).clip(0, 255).astype(np.uint8)
