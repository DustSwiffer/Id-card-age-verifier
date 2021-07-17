import Settings
import cv2
import numpy as np
import math

settings = Settings.Settings()
face_cascade = cv2.CascadeClassifier('config/face_detector.xml')


def Find(videoFramePath, idCardPath):
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

        scores = []
        for (x, y, w, h) in facesInIdCard:
            count += 1
            roiGrayIdCard = grayIdCard[y:y + h, x:x + w]

            score = cv2.matchTemplate(roiGrayIdCard, resizedVideoFrameRoI, cv2.TM_CCOEFF_NORMED).max()
            scores.append(score)

        return max(scores)


def IncreaseBrightnessOfSelfie(videoFramePath):
    hsv = cv2.cvtColor(videoFramePath, cv2.COLOR_BGR2HSV)

    hue, sat, val = cv2.split(hsv)

    mid = settings.Gamma
    mean = np.mean(val)
    gamma = math.log(mid * 255) / math.log(mean)

    valGamma = np.power(val, gamma).clip(0, 255).astype(np.uint8)

    hsv_gamma = cv2.merge([hue, sat, valGamma])

    gammaRGB = cv2.cvtColor(hsv_gamma, cv2.COLOR_HSV2BGR)
    grayVideoFrame = cv2.cvtColor(gammaRGB, cv2.COLOR_BGR2GRAY)

    return np.power(grayVideoFrame, gamma).clip(0, 255).astype(np.uint8)
