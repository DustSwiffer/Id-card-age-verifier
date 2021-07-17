import Settings
import cv2
import numpy as np
import math

settings = Settings.Settings()
face_cascade = cv2.CascadeClassifier('config/face_detector.xml')


def Find(videoFramePath, idCardPath):
    grayVideoFrame = IncreaseBrightnessOfSelfie(cv2.imread(videoFramePath))

    facesInVideoFrame = face_cascade.detectMultiScale(grayVideoFrame, 1.2, 4)

    grayIdCard = cv2.cvtColor(cv2.imread(idCardPath),
                              cv2.COLOR_BGR2GRAY)

    for (videoFrameX, videoFrameY, videoFrameW, videoFrameH) in facesInVideoFrame:
        roiGrayVideoFrame = grayVideoFrame[videoFrameY:videoFrameY + videoFrameH, videoFrameX:videoFrameX + videoFrameW]

        resizedVideoFrameRoI = cv2.resize(roiGrayVideoFrame,
                                          (int(roiGrayVideoFrame.shape[0] / 5),
                                           int(roiGrayVideoFrame.shape[1] / 5)))

        scores = []
        for (x, y, w, h) in face_cascade.detectMultiScale(grayIdCard, 1.2, 3):
            roiGrayIdCard = grayIdCard[y:y + h, x:x + w]

            scores.append(cv2.matchTemplate(roiGrayIdCard, resizedVideoFrameRoI, cv2.TM_CCOEFF_NORMED).max())

        return max(scores)


def IncreaseBrightnessOfSelfie(videoFramePath):
    hsv = cv2.cvtColor(videoFramePath, cv2.COLOR_BGR2HSV)

    hue, sat, val = cv2.split(hsv)

    gamma = math.log(settings.Gamma * 255) / math.log(np.mean(val))

    valGamma = np.power(val, gamma).clip(0, 255).astype(np.uint8)
    gammaRGB = cv2.cvtColor(cv2.merge([hue, sat, valGamma]), cv2.COLOR_HSV2BGR)

    return np.power(cv2.cvtColor(gammaRGB, cv2.COLOR_BGR2GRAY), gamma).clip(0, 255).astype(np.uint8)
